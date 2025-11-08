CREATE TABLE `AI Controller` (
  `ailD` <type>,
  `monitoredPlantIDs` <type>,
  `algorithmsUsed` <type>,
  `status` <type>,
  `lastAction` <type>,
  PRIMARY KEY (`ailD`)
);

CREATE TABLE `Water Filtration Plant` (
  `plantID` <type>,
  `location` <type>,
  `filtrationType` <type>,
  `aiMonitorID` <type>,
  `operationalStatus` <type>,
  PRIMARY KEY (`plantID`)
);

CREATE TABLE `Water Quality Sensor` (
  `sensorID` <type>,
  `plantID` <type>,
  `location` <type>,
  `pHLevel` <type>,
  `turbidity` <type>,
  `contaminantLevel` <type>,
  `temperature` <type>,
  `corrosionIndicator` <type>,
  `lastReadTime` <type>,
  PRIMARY KEY (`sensorID`)
);

CREATE TABLE `Filtration Process` (
  `processID` <type>,
  `plantID` <type>,
  `processType` <type>,
  `status` <type>,
  `lastMaintenanceDate` <type>,
  `filterEfficiency` <type>,
  PRIMARY KEY (`processID`)
);

CREATE TABLE `Pipeline Infrastructure` (
  `pipelineID` <type>,
  `plantID` <type>,
  `location` <type>,
  `pipeMaterial` <type>,
  `installDate` <type>,
  `rustLevel` <type>,
  `pressureLevel` <type>,
  `lastInspectionDate` <type>,
  `leakDetected` <type>,
  `status` <type>,
  PRIMARY KEY (`pipelineID`)
);

CREATE TABLE `Alert/Notification` (
  `alertID` <type>,
  `relatedPlantID` <type>,
  `relatedPipelineID` <type>,
  `alertType` <type>,
  `alertLevel` <type>,
  `alertDate` <type>,
  `actionTaken` <type>,
  PRIMARY KEY (`alertID`),
  FOREIGN KEY (`relatedPipelineID`)
      REFERENCES `Pipeline Infrastructure`(`lastInspectionDate`)
);

