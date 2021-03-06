from django.test import override_settings

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors
from vng_api_common.validators import (
    IsImmutableValidator, UniekeIdentificatieValidator, UntilTodayValidator,
    URLValidator
)

from brc.datamodel.tests.factories import BesluitFactory

from ..scopes import SCOPE_BESLUITEN_BIJWERKEN
from .utils import reverse, reverse_lazy

BESLUITTYPE = 'https://example.com/ztc/besluittype/abcd'


class BesluitValidationTests(JWTAuthMixin, APITestCase):
    url = reverse_lazy('besluit-list')
    heeft_alle_autorisaties = True

    @override_settings(LINK_FETCHER='vng_api_common.mocks.link_fetcher_404')
    def test_validate_urls_invalid(self):

        response = self.client.post(self.url, {
            'besluittype': 'https://example.com',
            'zaak': 'https://example.com',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        besluittype_error = get_validation_errors(response, 'besluittype')
        self.assertEqual(besluittype_error['code'], URLValidator.code)

        zaak_error = get_validation_errors(response, 'zaak')
        self.assertEqual(zaak_error['code'], URLValidator.code)

    def test_rsin_invalid(self):
        cases = [
            ('1234567', 'invalid-length'),
            ('12345678', 'invalid-length'),
            ('123456789', 'invalid'),
        ]

        for rsin, error_code in cases:
            with self.subTest(rsin=rsin, error_code=error_code):
                response = self.client.post(self.url, {
                    'verantwoordelijkeOrganisatie': rsin,
                })

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                error = get_validation_errors(response, 'verantwoordelijkeOrganisatie')
                self.assertEqual(error['code'], error_code)

    @freeze_time('2018-09-06T12:08+0200')
    def test_future_datum(self):
        response = self.client.post(self.url, {
            'datum': '2018-09-07',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, 'datum')
        self.assertEqual(error['code'], UntilTodayValidator.code)

    @override_settings(LINK_FETCHER='vng_api_common.mocks.link_fetcher_200')
    def test_duplicate_rsin_identificatie(self):
        besluit = BesluitFactory.create(identificatie='123456')

        response = self.client.post(self.url, {
            'verantwoordelijkeOrganisatie': besluit.verantwoordelijke_organisatie,
            'identificatie': '123456',

            'besluittype': 'https://example.com/ztc/besluittype/abcd',
            'zaak': 'https://example.com/zrc/zaken/1234',
            'datum': '2018-09-06',
            'ingangsdatum': '2018-10-01',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, 'identificatie')
        self.assertEqual(error['code'], UniekeIdentificatieValidator.code)

    def test_change_immutable_fields(self):
        besluit = BesluitFactory.create(identificatie='123456', besluittype=BESLUITTYPE)
        besluit2 = BesluitFactory.create(identificatie='123456', besluittype=BESLUITTYPE)

        url = reverse('besluit-detail', kwargs={'uuid': besluit.uuid})

        response = self.client.patch(url, {
            'verantwoordelijkeOrganisatie': besluit2.verantwoordelijke_organisatie,
            'identificatie': '123456789',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        identificatie_error = get_validation_errors(response, 'identificatie')
        self.assertEqual(identificatie_error['code'], IsImmutableValidator.code)

        verantwoordelijke_organisatie_error = get_validation_errors(response, 'verantwoordelijkeOrganisatie')
        self.assertEqual(verantwoordelijke_organisatie_error['code'], IsImmutableValidator.code)


class BesluitInformatieObjectTests(JWTAuthMixin, APITestCase):

    heeft_alle_autorisaties = True

    @override_settings(
        LINK_FETCHER='vng_api_common.mocks.link_fetcher_404',
        ZDS_CLIENT_CLASS='vng_api_common.mocks.ObjectInformatieObjectClient'
    )
    def test_validate_informatieobject_invalid(self):
        besluit = BesluitFactory.create(besluittype=BESLUITTYPE)
        url = reverse('besluitinformatieobject-list', kwargs={'besluit_uuid': besluit.uuid})

        response = self.client.post(url, {
            'informatieobject': 'https://foo.bar/123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, 'informatieobject')
        self.assertEqual(error['code'], URLValidator.code)
