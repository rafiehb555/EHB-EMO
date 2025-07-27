// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/**
 * @title HealthcareRegistry
 * @dev Healthcare patient data registry with HIPAA compliance
 * @author EHB Healthcare Platform
 */
contract HealthcareRegistry {
  // Events
  event PatientRegistered(
    address indexed patient,
    uint256 patientId,
    string name
  );
  event MedicalRecordAdded(
    uint256 indexed patientId,
    uint256 recordId,
    string recordHash
  );
  event AccessGranted(address indexed doctor, uint256 indexed patientId);
  event AccessRevoked(address indexed doctor, uint256 indexed patientId);
  event EmergencyAccessGranted(
    address indexed emergencyProvider,
    uint256 indexed patientId
  );

  // Structs
  struct Patient {
    uint256 patientId;
    string name;
    uint256 dateOfBirth;
    string bloodType;
    bool isActive;
    uint256 registrationDate;
    address patientAddress;
  }

  struct MedicalRecord {
    uint256 recordId;
    uint256 patientId;
    string recordHash;
    uint256 timestamp;
    address doctorAddress;
    string recordType;
    bool isEmergency;
  }

  struct Doctor {
    address doctorAddress;
    string name;
    string licenseNumber;
    bool isActive;
    uint256 registrationDate;
  }

  // State variables
  address public owner;
  uint256 private _nextPatientId = 1;
  uint256 private _nextRecordId = 1;

  mapping(uint256 => Patient) public patients;
  mapping(uint256 => MedicalRecord) public medicalRecords;
  mapping(address => Doctor) public doctors;
  mapping(address => uint256) public patientAddressToId;
  mapping(uint256 => address[]) public patientDoctors;
  mapping(address => uint256[]) public doctorPatients;
  mapping(uint256 => MedicalRecord[]) public patientRecords;

  // Modifiers
  modifier onlyOwner() {
    require(msg.sender == owner, 'Only owner can perform this action');
    _;
  }

  modifier onlyDoctor() {
    require(
      doctors[msg.sender].isActive,
      'Only registered doctors can perform this action'
    );
    _;
  }

  modifier onlyPatientOrDoctor(uint256 patientId) {
    require(
      patientAddressToId[msg.sender] == patientId ||
        isDoctorForPatient(msg.sender, patientId),
      'Only patient or authorized doctor can perform this action'
    );
    _;
  }

  modifier onlyEmergencyProvider() {
    require(
      doctors[msg.sender].isActive,
      'Only registered emergency providers can perform this action'
    );
    _;
  }

  constructor() {
    owner = msg.sender;
  }

  /**
   * @dev Register a new patient
   * @param name Patient's full name
   * @param dateOfBirth Patient's date of birth (timestamp)
   * @param bloodType Patient's blood type
   */
  function registerPatient(
    string memory name,
    uint256 dateOfBirth,
    string memory bloodType
  ) external {
    require(bytes(name).length > 0, 'Name cannot be empty');
    require(dateOfBirth > 0, 'Invalid date of birth');
    require(patientAddressToId[msg.sender] == 0, 'Patient already registered');

    uint256 patientId = _nextPatientId++;

    patients[patientId] = Patient({
      patientId: patientId,
      name: name,
      dateOfBirth: dateOfBirth,
      bloodType: bloodType,
      isActive: true,
      registrationDate: block.timestamp,
      patientAddress: msg.sender
    });

    patientAddressToId[msg.sender] = patientId;

    emit PatientRegistered(msg.sender, patientId, name);
  }

  /**
   * @dev Register a new doctor
   * @param doctorAddress Doctor's address
   * @param name Doctor's full name
   * @param licenseNumber Medical license number
   */
  function registerDoctor(
    address doctorAddress,
    string memory name,
    string memory licenseNumber
  ) external onlyOwner {
    require(bytes(name).length > 0, 'Name cannot be empty');
    require(bytes(licenseNumber).length > 0, 'License number cannot be empty');
    require(!doctors[doctorAddress].isActive, 'Doctor already registered');

    doctors[doctorAddress] = Doctor({
      doctorAddress: doctorAddress,
      name: name,
      licenseNumber: licenseNumber,
      isActive: true,
      registrationDate: block.timestamp
    });
  }

  /**
   * @dev Add medical record for a patient
   * @param patientId Patient's ID
   * @param recordHash Hash of the medical record
   * @param recordType Type of medical record
   */
  function addMedicalRecord(
    uint256 patientId,
    string memory recordHash,
    string memory recordType
  ) external onlyDoctor {
    require(patients[patientId].isActive, 'Patient not found or inactive');
    require(bytes(recordHash).length > 0, 'Record hash cannot be empty');
    require(
      isDoctorForPatient(msg.sender, patientId),
      'Doctor not authorized for this patient'
    );

    uint256 recordId = _nextRecordId++;

    MedicalRecord memory newRecord = MedicalRecord({
      recordId: recordId,
      patientId: patientId,
      recordHash: recordHash,
      timestamp: block.timestamp,
      doctorAddress: msg.sender,
      recordType: recordType,
      isEmergency: false
    });

    medicalRecords[recordId] = newRecord;
    patientRecords[patientId].push(newRecord);

    emit MedicalRecordAdded(patientId, recordId, recordHash);
  }

  /**
   * @dev Add emergency medical record
   * @param patientId Patient's ID
   * @param recordHash Hash of the medical record
   * @param recordType Type of medical record
   */
  function addEmergencyRecord(
    uint256 patientId,
    string memory recordHash,
    string memory recordType
  ) external onlyEmergencyProvider {
    require(patients[patientId].isActive, 'Patient not found or inactive');
    require(bytes(recordHash).length > 0, 'Record hash cannot be empty');

    uint256 recordId = _nextRecordId++;

    MedicalRecord memory newRecord = MedicalRecord({
      recordId: recordId,
      patientId: patientId,
      recordHash: recordHash,
      timestamp: block.timestamp,
      doctorAddress: msg.sender,
      recordType: recordType,
      isEmergency: true
    });

    medicalRecords[recordId] = newRecord;
    patientRecords[patientId].push(newRecord);

    emit MedicalRecordAdded(patientId, recordId, recordHash);
    emit EmergencyAccessGranted(msg.sender, patientId);
  }

  /**
   * @dev Grant access to a doctor for a patient
   * @param doctorAddress Doctor's address
   * @param patientId Patient's ID
   */
  function grantAccess(address doctorAddress, uint256 patientId) external {
    require(patients[patientId].isActive, 'Patient not found or inactive');
    require(doctors[doctorAddress].isActive, 'Doctor not found or inactive');
    require(
      patientAddressToId[msg.sender] == patientId || msg.sender == owner,
      'Only patient or owner can grant access'
    );

    // Check if doctor already has access
    for (uint i = 0; i < patientDoctors[patientId].length; i++) {
      if (patientDoctors[patientId][i] == doctorAddress) {
        return; // Already has access
      }
    }

    patientDoctors[patientId].push(doctorAddress);
    doctorPatients[doctorAddress].push(patientId);

    emit AccessGranted(doctorAddress, patientId);
  }

  /**
   * @dev Revoke access from a doctor for a patient
   * @param doctorAddress Doctor's address
   * @param patientId Patient's ID
   */
  function revokeAccess(address doctorAddress, uint256 patientId) external {
    require(
      patientAddressToId[msg.sender] == patientId || msg.sender == owner,
      'Only patient or owner can revoke access'
    );

    // Remove doctor from patient's doctors list
    for (uint i = 0; i < patientDoctors[patientId].length; i++) {
      if (patientDoctors[patientId][i] == doctorAddress) {
        patientDoctors[patientId][i] = patientDoctors[patientId][
          patientDoctors[patientId].length - 1
        ];
        patientDoctors[patientId].pop();
        break;
      }
    }

    // Remove patient from doctor's patients list
    for (uint i = 0; i < doctorPatients[doctorAddress].length; i++) {
      if (doctorPatients[doctorAddress][i] == patientId) {
        doctorPatients[doctorAddress][i] = doctorPatients[doctorAddress][
          doctorPatients[doctorAddress].length - 1
        ];
        doctorPatients[doctorAddress].pop();
        break;
      }
    }

    emit AccessRevoked(doctorAddress, patientId);
  }

  /**
   * @dev Check if doctor has access to patient
   * @param doctorAddress Doctor's address
   * @param patientId Patient's ID
   * @return bool True if doctor has access
   */
  function isDoctorForPatient(
    address doctorAddress,
    uint256 patientId
  ) public view returns (bool) {
    for (uint i = 0; i < patientDoctors[patientId].length; i++) {
      if (patientDoctors[patientId][i] == doctorAddress) {
        return true;
      }
    }
    return false;
  }

  /**
   * @dev Get patient information
   * @param patientId Patient's ID
   * @return Patient struct
   */
  function getPatient(
    uint256 patientId
  ) external view returns (Patient memory) {
    return patients[patientId];
  }

  /**
   * @dev Get patient's medical records
   * @param patientId Patient's ID
   * @return MedicalRecord array
   */
  function getPatientRecords(
    uint256 patientId
  ) external view returns (MedicalRecord[] memory) {
    return patientRecords[patientId];
  }

  /**
   * @dev Get doctor information
   * @param doctorAddress Doctor's address
   * @return Doctor struct
   */
  function getDoctor(
    address doctorAddress
  ) external view returns (Doctor memory) {
    return doctors[doctorAddress];
  }

  /**
   * @dev Get patient's authorized doctors
   * @param patientId Patient's ID
   * @return address array of doctor addresses
   */
  function getPatientDoctors(
    uint256 patientId
  ) external view returns (address[] memory) {
    return patientDoctors[patientId];
  }

  /**
   * @dev Get doctor's patients
   * @param doctorAddress Doctor's address
   * @return uint256 array of patient IDs
   */
  function getDoctorPatients(
    address doctorAddress
  ) external view returns (uint256[] memory) {
    return doctorPatients[doctorAddress];
  }

  /**
   * @dev Get patient ID by address
   * @param patientAddress Patient's address
   * @return uint256 Patient ID
   */
  function getPatientIdByAddress(
    address patientAddress
  ) external view returns (uint256) {
    return patientAddressToId[patientAddress];
  }

  /**
   * @dev Get total number of patients
   * @return uint256 Total patient count
   */
  function getTotalPatients() external view returns (uint256) {
    return _nextPatientId - 1;
  }

  /**
   * @dev Get total number of medical records
   * @return uint256 Total record count
   */
  function getTotalRecords() external view returns (uint256) {
    return _nextRecordId - 1;
  }
}
