===========
Wijzigingen
===========

0.9.0 (2019-04-16)
==================

API-lab release

* Improved homepage layout, using vng-api-common boilerplate
* Bumped to latest bugfix release of gemma-zds-client

Breaking changes
----------------

* Flattened the ``kenmerken`` in notifications sent from a list of objects with
  one key-value to a single object with multiple key-value pairs.
  Requires the NC to be at version 0.4.0 or higher.

  Old:

  .. code-block:: json

  {
    "kenmerken": [
      {"key1": "value1"},
      {"key2": "value2"},
    ]
  }

  New:

  .. code-block:: json

  {
    "kenmerken": {
      "key1": "value1",
      "key2": "value2",
    }
  }

0.8.0 (2019-04-04)
==================

Removed zds-schema from the project

* Fixed a bug because of missing entry in INSTALLED_APPS

0.7.2 (2019-04-04)
==================

Added missing application to INSTALLED_APPS

0.7.1 (2019-04-04)
==================

Added missing markup/markdown dependencies

0.7.0 (2019-04-04)
==================

Feature release: notifications support

* Included URL to EUPL 1.2 license in API spec
* added notifications machinery. Configure the NC to use in the admin and then
  run ``python src/manage.py register_kanaal`` to register the notifications
  exchange and be able to publish events.
* added notifications documentation.

Breaking changes
----------------

* replaced zds-schema with vng-api-common. Run
  ``python src/manage.py migrate_from_zds_schema`` on existing installs to
  complete the migration.

0.6.2 (2019-03-05)
==================

Bugfix release

* Bump zds-client via zds-schema

0.6.1 (2019-02-28)
==================

Fix operation -> scopes mapping

* Enforced required scopes
* Ensured scopes end up in OAS

0.6.0 (2019-02-27)
==================

Archiving feature release

* added support for ``DELETE`` requests to ``Besluit`` resource
* added support for ``DELETE`` requests to ``BesluitInformatieObjectViewSet`` resource

0.5.5 (2018-12-13)
==================

Bump Django and urllib

* urllib3<=1.22 has a CVE
* use latest patch release of Django 2.0

0.5.4 (2018-12-11)
==================

Small bugfixes

* Fixed validator using newer gemma-zds-client
* Added a name for the session cookie to preserve sessions on the same domain
  between components.
* Added missing Api-Version header
* Added missing Location header to OAS


0.5.0 (2018-11-27)
==================

Stap naar volwassenere API

* HTTP 400 errors op onbekende/invalide filter-parameters
* Docker container beter te customizen via environment variables

Breaking change
---------------

De ``Authorization`` headers is veranderd van formaat. In plaats van ``<jwt>``
is het nu ``Bearer <jwt>`` geworden.


0.4.4 (2018-11-27)
==================

Autorisatie: bugfix

Bij het aanroepen van ZTC en ZRC werd er geen gebruik gemaakt van de autorisatie
headers.

0.4.3 (2018-11-26)
==================

Bump naar zds-schema 0.14.0 om JWT decode-problemen correct af te vangen.

0.4.2 (2018-11-22)
==================

DSO API-srategie fix

Foutberichten bevatten een ``type`` key. De waarde van deze key begint niet
langer incorrect met ``"URI: "``.

0.4.1 (2018-11-21)
==================

Fix missing auth configuration from 0.4.0

0.4.0 (2018-11-21)
==================

Autorisatie-feature release

* Voeg JWT client/secret management toe
* Opzet credentialstore om URLs te kunnen valideren met auth/autz

0.3.0 (2018-11-19)
==================

Aanpassingen na RGBZ-toetsing

Features
--------

* ``CORS``-support toegevoegd

Breaking changes
----------------

* ``Besluit.datum`` als datum in plaats van datetime
* Geen limitatie op lengte van ``Besluit.toelichting``
* ``identificatie`` en ``verantwoorelijkeOrganisatie`` zijn immutable
* ``vervalredenWeergave`` is niet langer een enum - de mapping staat in de
  beschrijving van ``vervalreden``.


0.2.1 (2018-10-25)
==================

Bugfix in infrastructuur

* nodejs deps toegevoegd (swagger2openapi)

0.2.0 (2018-10-02)
==================

Besluit-informatieobject relatie resource toegevoegd

* fix MIME-types voor error responses
* ``besluitinfomratieobject`` als nested resource toegevoegd op besluiten
* validaties op ``BesluitInformatieObject`` toegevoegd

0.1.1 (2018-09-12)
==================

* Fix missing ``Accept-Crs`` header in ZAAK-url validator
* Added license


0.1.0 (2018-09-10)
==================

* Eerste aanzet besluitregistratie
