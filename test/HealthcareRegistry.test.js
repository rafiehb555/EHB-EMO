const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("HealthcareRegistry", function () {
  let healthcareRegistry;
  let owner;
  let patient1;
  let patient2;
  let doctor1;
  let doctor2;
  let emergencyProvider;

  beforeEach(async function () {
    [owner, patient1, patient2, doctor1, doctor2, emergencyProvider] = await ethers.getSigners();
    
    const HealthcareRegistry = await ethers.getContractFactory("HealthcareRegistry");
    healthcareRegistry = await HealthcareRegistry.deploy();
    await healthcareRegistry.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await healthcareRegistry.owner()).to.equal(owner.address);
    });

    it("Should start with zero patients", async function () {
      expect(await healthcareRegistry.getTotalPatients()).to.equal(0);
    });

    it("Should start with zero records", async function () {
      expect(await healthcareRegistry.getTotalRecords()).to.equal(0);
    });
  });

  describe("Patient Registration", function () {
    it("Should register a new patient", async function () {
      const patientName = "John Doe";
      const dateOfBirth = 946684800; // 2000-01-01
      const bloodType = "O+";

      await expect(healthcareRegistry.connect(patient1).registerPatient(
        patientName,
        dateOfBirth,
        bloodType
      ))
        .to.emit(healthcareRegistry, "PatientRegistered")
        .withArgs(patient1.address, 1, patientName);

      const patient = await healthcareRegistry.getPatient(1);
      expect(patient.name).to.equal(patientName);
      expect(patient.dateOfBirth).to.equal(dateOfBirth);
      expect(patient.bloodType).to.equal(bloodType);
      expect(patient.isActive).to.be.true;
      expect(patient.patientAddress).to.equal(patient1.address);
    });

    it("Should not allow empty name", async function () {
      await expect(
        healthcareRegistry.connect(patient1).registerPatient("", 946684800, "O+")
      ).to.be.revertedWith("Name cannot be empty");
    });

    it("Should not allow invalid date of birth", async function () {
      await expect(
        healthcareRegistry.connect(patient1).registerPatient("John Doe", 0, "O+")
      ).to.be.revertedWith("Invalid date of birth");
    });

    it("Should not allow duplicate registration", async function () {
      await healthcareRegistry.connect(patient1).registerPatient("John Doe", 946684800, "O+");
      
      await expect(
        healthcareRegistry.connect(patient1).registerPatient("Jane Doe", 946684800, "A+")
      ).to.be.revertedWith("Patient already registered");
    });
  });

  describe("Doctor Registration", function () {
    it("Should register a new doctor", async function () {
      const doctorName = "Dr. Smith";
      const licenseNumber = "MD123456";

      await healthcareRegistry.connect(owner).registerDoctor(doctor1.address, doctorName, licenseNumber);

      const doctor = await healthcareRegistry.getDoctor(doctor1.address);
      expect(doctor.name).to.equal(doctorName);
      expect(doctor.licenseNumber).to.equal(licenseNumber);
      expect(doctor.isActive).to.be.true;
    });

    it("Should not allow non-owner to register doctor", async function () {
      await expect(
        healthcareRegistry.connect(patient1).registerDoctor(doctor1.address, "Dr. Smith", "MD123456")
      ).to.be.revertedWith("Only owner can perform this action");
    });

    it("Should not allow empty doctor name", async function () {
      await expect(
        healthcareRegistry.connect(owner).registerDoctor(doctor1.address, "", "MD123456")
      ).to.be.revertedWith("Name cannot be empty");
    });

    it("Should not allow empty license number", async function () {
      await expect(
        healthcareRegistry.connect(owner).registerDoctor(doctor1.address, "Dr. Smith", "")
      ).to.be.revertedWith("License number cannot be empty");
    });
  });

  describe("Medical Records", function () {
    beforeEach(async function () {
      // Register patient and doctor
      await healthcareRegistry.connect(patient1).registerPatient("John Doe", 946684800, "O+");
      await healthcareRegistry.connect(owner).registerDoctor(doctor1.address, "Dr. Smith", "MD123456");
      
      // Grant access to doctor
      await healthcareRegistry.connect(patient1).grantAccess(doctor1.address, 1);
    });

    it("Should add medical record", async function () {
      const recordHash = "QmHash123456789";
      const recordType = "Diagnosis";

      await expect(healthcareRegistry.connect(doctor1).addMedicalRecord(
        1,
        recordHash,
        recordType
      ))
        .to.emit(healthcareRegistry, "MedicalRecordAdded")
        .withArgs(1, 1, recordHash);

      const records = await healthcareRegistry.getPatientRecords(1);
      expect(records.length).to.equal(1);
      expect(records[0].recordHash).to.equal(recordHash);
      expect(records[0].recordType).to.equal(recordType);
      expect(records[0].isEmergency).to.be.false;
    });

    it("Should not allow unauthorized doctor to add record", async function () {
      await healthcareRegistry.connect(owner).registerDoctor(doctor2.address, "Dr. Jones", "MD789012");
      
      await expect(
        healthcareRegistry.connect(doctor2).addMedicalRecord(1, "QmHash123", "Diagnosis")
      ).to.be.revertedWith("Doctor not authorized for this patient");
    });

    it("Should not allow adding record for non-existent patient", async function () {
      await expect(
        healthcareRegistry.connect(doctor1).addMedicalRecord(999, "QmHash123", "Diagnosis")
      ).to.be.revertedWith("Patient not found or inactive");
    });

    it("Should not allow empty record hash", async function () {
      await expect(
        healthcareRegistry.connect(doctor1).addMedicalRecord(1, "", "Diagnosis")
      ).to.be.revertedWith("Record hash cannot be empty");
    });
  });

  describe("Emergency Records", function () {
    beforeEach(async function () {
      await healthcareRegistry.connect(patient1).registerPatient("John Doe", 946684800, "O+");
      await healthcareRegistry.connect(owner).registerDoctor(emergencyProvider.address, "Dr. Emergency", "MD999999");
    });

    it("Should add emergency record", async function () {
      const recordHash = "QmEmergencyHash";
      const recordType = "Emergency";

      await expect(healthcareRegistry.connect(emergencyProvider).addEmergencyRecord(
        1,
        recordHash,
        recordType
      ))
        .to.emit(healthcareRegistry, "MedicalRecordAdded")
        .withArgs(1, 1, recordHash);

      const records = await healthcareRegistry.getPatientRecords(1);
      expect(records.length).to.equal(1);
      expect(records[0].isEmergency).to.be.true;
    });
  });

  describe("Access Control", function () {
    beforeEach(async function () {
      await healthcareRegistry.connect(patient1).registerPatient("John Doe", 946684800, "O+");
      await healthcareRegistry.connect(owner).registerDoctor(doctor1.address, "Dr. Smith", "MD123456");
      await healthcareRegistry.connect(owner).registerDoctor(doctor2.address, "Dr. Jones", "MD789012");
    });

    it("Should grant access to doctor", async function () {
      await expect(healthcareRegistry.connect(patient1).grantAccess(doctor1.address, 1))
        .to.emit(healthcareRegistry, "AccessGranted")
        .withArgs(doctor1.address, 1);

      expect(await healthcareRegistry.isDoctorForPatient(doctor1.address, 1)).to.be.true;
    });

    it("Should revoke access from doctor", async function () {
      await healthcareRegistry.connect(patient1).grantAccess(doctor1.address, 1);
      
      await expect(healthcareRegistry.connect(patient1).revokeAccess(doctor1.address, 1))
        .to.emit(healthcareRegistry, "AccessRevoked")
        .withArgs(doctor1.address, 1);

      expect(await healthcareRegistry.isDoctorForPatient(doctor1.address, 1)).to.be.false;
    });

    it("Should not allow non-patient to grant access", async function () {
      await expect(
        healthcareRegistry.connect(patient2).grantAccess(doctor1.address, 1)
      ).to.be.revertedWith("Only patient or owner can grant access");
    });

    it("Should allow owner to grant access", async function () {
      await expect(healthcareRegistry.connect(owner).grantAccess(doctor1.address, 1))
        .to.emit(healthcareRegistry, "AccessGranted")
        .withArgs(doctor1.address, 1);
    });
  });

  describe("Data Retrieval", function () {
    beforeEach(async function () {
      await healthcareRegistry.connect(patient1).registerPatient("John Doe", 946684800, "O+");
      await healthcareRegistry.connect(patient2).registerPatient("Jane Doe", 946684800, "A+");
      await healthcareRegistry.connect(owner).registerDoctor(doctor1.address, "Dr. Smith", "MD123456");
    });

    it("Should get patient by ID", async function () {
      const patient = await healthcareRegistry.getPatient(1);
      expect(patient.name).to.equal("John Doe");
      expect(patient.patientAddress).to.equal(patient1.address);
    });

    it("Should get patient ID by address", async function () {
      const patientId = await healthcareRegistry.getPatientIdByAddress(patient1.address);
      expect(patientId).to.equal(1);
    });

    it("Should get doctor information", async function () {
      const doctor = await healthcareRegistry.getDoctor(doctor1.address);
      expect(doctor.name).to.equal("Dr. Smith");
      expect(doctor.licenseNumber).to.equal("MD123456");
    });

    it("Should get patient's doctors", async function () {
      await healthcareRegistry.connect(patient1).grantAccess(doctor1.address, 1);
      
      const doctors = await healthcareRegistry.getPatientDoctors(1);
      expect(doctors.length).to.equal(1);
      expect(doctors[0]).to.equal(doctor1.address);
    });

    it("Should get doctor's patients", async function () {
      await healthcareRegistry.connect(patient1).grantAccess(doctor1.address, 1);
      
      const patients = await healthcareRegistry.getDoctorPatients(doctor1.address);
      expect(patients.length).to.equal(1);
      expect(patients[0]).to.equal(1);
    });
  });

  describe("Statistics", function () {
    it("Should track total patients correctly", async function () {
      expect(await healthcareRegistry.getTotalPatients()).to.equal(0);
      
      await healthcareRegistry.connect(patient1).registerPatient("John Doe", 946684800, "O+");
      expect(await healthcareRegistry.getTotalPatients()).to.equal(1);
      
      await healthcareRegistry.connect(patient2).registerPatient("Jane Doe", 946684800, "A+");
      expect(await healthcareRegistry.getTotalPatients()).to.equal(2);
    });

    it("Should track total records correctly", async function () {
      expect(await healthcareRegistry.getTotalRecords()).to.equal(0);
      
      await healthcareRegistry.connect(patient1).registerPatient("John Doe", 946684800, "O+");
      await healthcareRegistry.connect(owner).registerDoctor(doctor1.address, "Dr. Smith", "MD123456");
      await healthcareRegistry.connect(patient1).grantAccess(doctor1.address, 1);
      await healthcareRegistry.connect(doctor1).addMedicalRecord(1, "QmHash1", "Diagnosis");
      
      expect(await healthcareRegistry.getTotalRecords()).to.equal(1);
      
      await healthcareRegistry.connect(doctor1).addMedicalRecord(1, "QmHash2", "Treatment");
      expect(await healthcareRegistry.getTotalRecords()).to.equal(2);
    });
  });
}); 