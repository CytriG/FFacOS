

DROP TABLE IF EXISTS `clients`;
CREATE TABLE `clients` (
  `Id` int NOT NULL ,
  `Nom` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `Prenoms` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `Civilite` int NOT NULL DEFAULT '1',
  `NomUsage` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `DateNaissance` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `PaysNaissance` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `DepNaissance` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `CodeVilleNaissance` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `VilleNaissance` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `Tel` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `Email` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `AdresseNumVoie` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `AdresseLettreVoie` varchar(100) DEFAULT 'NotDefined',
  `AdresseCodeVoie` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `AdresseVoie` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `AdresseComplement` varchar(100) DEFAULT 'NotDefined',
  `AdresseLieuDit` varchar(100) DEFAULT 'NotDefined',
  `AdresseVille` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `AdresseCodeVille` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `AdresseCodePostal` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `AdresseCodePays` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `BanqueBIC` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `BanqueIBAN` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `BanqueTitulaire` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `IdUrssaf` varchar(100) DEFAULT 'NotDefined',
  PRIMARY KEY (`Id`)
) ;


DROP TABLE IF EXISTS `cours`;

CREATE TABLE `cours` (
  `Id` bigint NOT NULL ,
  `Niveau` varchar(10) DEFAULT 'NotDefined',
  `NHourFacturee` decimal(10,2) DEFAULT '0.00',
  `NHourReal` decimal(10,2) DEFAULT '0.00',
  `SurPlace` tinyint(1) DEFAULT '1',
  `NHourPreparation` decimal(10,2) DEFAULT '0.00',
  `StudentId` bigint NOT NULL,
  `Date` datetime NOT NULL,
  `FactureId` bigint DEFAULT NULL,
  `HourPriceHT` decimal(10,2) NOT NULL DEFAULT '50.00',
  PRIMARY KEY (`Id`)
) ;


DROP TABLE IF EXISTS `demanedpaiementurssaf`;

CREATE TABLE `demanedpaiementurssaf` (
  `Id` bigint NOT NULL ,
  `IdFacture` bigint NOT NULL,
  `IdClientUrssaf` varchar(100) DEFAULT NULL,
  `IdUrssaf` varchar(100) DEFAULT NULL,
  `NumFactureUrssaf` varchar(100) DEFAULT NULL,
  `Status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ;

DROP TABLE IF EXISTS `factures`;

CREATE TABLE `factures` (
  `Id` bigint NOT NULL ,
  `IdTiersFacturation` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `IdClient` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `NumFacture` varchar(100) NOT NULL DEFAULT '1',
  `DateFacture` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `DateDebutEmploi` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `DateFinEmploi` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `Acompte` decimal(10,2) DEFAULT '0.00',
  `DateAcompte` varchar(100) DEFAULT 'NotDefined',
  `MontantTTC` decimal(10,2) NOT NULL DEFAULT '0.00',
  `MontantHT` decimal(10,2) NOT NULL DEFAULT '0.00',
  `IdUrssaf` varchar(100) DEFAULT NULL,
  `StatutDemandePaiementUrssaf` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ;


DROP TABLE IF EXISTS `presta`;

CREATE TABLE `presta` (
  `Id` bigint NOT NULL ,
  `CodeActivitePresta` varchar(100) DEFAULT 'NotDefined',
  `CodeNature` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `Quantite` decimal(10,2) NOT NULL DEFAULT '1.00',
  `Unite` varchar(100) NOT NULL DEFAULT 'HEURE',
  `MontantUnitaireTTC` decimal(10,2) NOT NULL DEFAULT '0.00',
  `MontantTTC` decimal(10,2) NOT NULL DEFAULT '1.00',
  `MontantHT` decimal(10,2) NOT NULL DEFAULT '1.00',
  `MontantTVA` decimal(10,2) NOT NULL DEFAULT '1.00',
  `Complement1` text,
  `Complement2` varchar(100) DEFAULT NULL,
  `IdFacture` bigint DEFAULT NULL,
  `IdClients` bigint NOT NULL,
  PRIMARY KEY (`Id`)
) ;


DROP TABLE IF EXISTS `students`;

CREATE TABLE `students` (
  `Id` bigint NOT NULL ,
  `Nom` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `Prenoms` varchar(100) NOT NULL DEFAULT 'NotDefined',
  `ClientId` bigint NOT NULL,
  PRIMARY KEY (`Id`)
) ;
