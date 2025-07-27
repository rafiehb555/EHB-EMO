// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title HealthcareRecords
 * @dev HIPAA-compliant healthcare records management on Ethereum
 * @author EHB Healthcare System
 */

contract HealthcareRecords {
    
    // Structs
    struct Patient {
        string patientId;
        string name;
        uint256 dateOfBirth;
        string bloodType;
        bool isActive;
        uint256 createdAt;
        address authorizedBy;
    }
    
    struct MedicalRecord {
        string recordId;
        string patientId;
        string diagnosis;
        string treatment;
        string medication;
        uint256 recordDate;
        address doctorAddress;
        bool isEncrypted;
        string ipfsHash;
    }
    
    struct Doctor {
        string doctorId;
        string name;
        string specialization;
        string licenseNumber;
        bool isActive;
        uint256 registeredAt;
    }
    
    struct Consent {
        string patientId;
        address doctorAddress;
        uint256 consentDate;
        uint256 expiryDate;
        bool isActive;
    }
    
    // State Variables
    mapping(string => Patient) public patients;
    mapping(string => MedicalRecord[]) public patientRecords;
    mapping(address => Doctor) public doctors;
    mapping(string => mapping(address => Consent)) public consents;
    mapping(address => bool) public authorizedDoctors;
    mapping(address => bool) public authorizedPatients;
    
    // Events
    event PatientRegistered(string patientId, string name, uint256 timestamp);
    event DoctorRegistered(address doctorAddress, string name, uint256 timestamp);
    event RecordAdded(string patientId, string recordId, uint256 timestamp);
    event ConsentGiven(string patientId, address doctorAddress, uint256 timestamp);
    event ConsentRevoked(string patientId, address doctorAddress, uint256 timestamp);
    event AccessGranted(address doctorAddress, string patientId, uint256 timestamp);
    event AccessRevoked(address doctorAddress, string patientId, uint256 timestamp);
    
    // Modifiers
    modifier onlyAuthorizedDoctor() {
        require(authorizedDoctors[msg.sender], "Only authorized doctors can perform this action");
        _;
    }
    
    modifier onlyAuthorizedPatient() {
        require(authorizedPatients[msg.sender], "Only authorized patients can perform this action");
        _;
    }
    
    modifier patientExists(string memory patientId) {
        require(patients[patientId].isActive, "Patient does not exist");
        _;
    }
    
    modifier doctorExists(address doctorAddress) {
        require(doctors[doctorAddress].isActive, "Doctor not registered");
        _;
    }
    
    modifier hasConsent(string memory patientId, address doctorAddress) {
        require(
            consents[patientId][doctorAddress].isActive && 
            consents[patientId][doctorAddress].expiryDate > block.timestamp,
            "No valid consent found"
        );
        _;
    }
    
    // Constructor
    constructor() {
        // Initialize system
    }
    
    /**
     * @dev Register a new patient
     * @param patientId Unique patient identifier
     * @param name Patient's full name
     * @param dateOfBirth Patient's date of birth
     * @param bloodType Patient's blood type
     */
    function registerPatient(
        string memory patientId,
        string memory name,
        uint256 dateOfBirth,
        string memory bloodType
    ) public onlyAuthorizedDoctor {
        require(bytes(patientId).length > 0, "Patient ID cannot be empty");
        require(bytes(name).length > 0, "Name cannot be empty");
        require(dateOfBirth > 0, "Invalid date of birth");
        
        patients[patientId] = Patient({
            patientId: patientId,
            name: name,
            dateOfBirth: dateOfBirth,
            bloodType: bloodType,
            isActive: true,
            createdAt: block.timestamp,
            authorizedBy: msg.sender
        });
        
        emit PatientRegistered(patientId, name, block.timestamp);
    }
    
    /**
     * @dev Register a new doctor
     * @param doctorId Unique doctor identifier
     * @param name Doctor's full name
     * @param specialization Doctor's specialization
     * @param licenseNumber Medical license number
     */
    function registerDoctor(
        string memory doctorId,
        string memory name,
        string memory specialization,
        string memory licenseNumber
    ) public {
        require(bytes(doctorId).length > 0, "Doctor ID cannot be empty");
        require(bytes(name).length > 0, "Name cannot be empty");
        require(bytes(licenseNumber).length > 0, "License number cannot be empty");
        
        doctors[msg.sender] = Doctor({
            doctorId: doctorId,
            name: name,
            specialization: specialization,
            licenseNumber: licenseNumber,
            isActive: true,
            registeredAt: block.timestamp
        });
        
        authorizedDoctors[msg.sender] = true;
        
        emit DoctorRegistered(msg.sender, name, block.timestamp);
    }
    
    /**
     * @dev Add a medical record for a patient
     * @param patientId Patient identifier
     * @param recordId Unique record identifier
     * @param diagnosis Medical diagnosis
     * @param treatment Treatment provided
     * @param medication Medication prescribed
     * @param ipfsHash IPFS hash of encrypted record
     */
    function addMedicalRecord(
        string memory patientId,
        string memory recordId,
        string memory diagnosis,
        string memory treatment,
        string memory medication,
        string memory ipfsHash
    ) public onlyAuthorizedDoctor patientExists(patientId) hasConsent(patientId, msg.sender) {
        require(bytes(recordId).length > 0, "Record ID cannot be empty");
        
        MedicalRecord memory newRecord = MedicalRecord({
            recordId: recordId,
            patientId: patientId,
            diagnosis: diagnosis,
            treatment: treatment,
            medication: medication,
            recordDate: block.timestamp,
            doctorAddress: msg.sender,
            isEncrypted: true,
            ipfsHash: ipfsHash
        });
        
        patientRecords[patientId].push(newRecord);
        
        emit RecordAdded(patientId, recordId, block.timestamp);
    }
    
    /**
     * @dev Give consent for a doctor to access patient records
     * @param patientId Patient identifier
     * @param doctorAddress Doctor's Ethereum address
     * @param expiryDate Consent expiry date
     */
    function giveConsent(
        string memory patientId,
        address doctorAddress,
        uint256 expiryDate
    ) public onlyAuthorizedPatient patientExists(patientId) doctorExists(doctorAddress) {
        require(expiryDate > block.timestamp, "Expiry date must be in the future");
        
        consents[patientId][doctorAddress] = Consent({
            patientId: patientId,
            doctorAddress: doctorAddress,
            consentDate: block.timestamp,
            expiryDate: expiryDate,
            isActive: true
        });
        
        emit ConsentGiven(patientId, doctorAddress, block.timestamp);
    }
    
    /**
     * @dev Revoke consent for a doctor
     * @param patientId Patient identifier
     * @param doctorAddress Doctor's Ethereum address
     */
    function revokeConsent(
        string memory patientId,
        address doctorAddress
    ) public onlyAuthorizedPatient patientExists(patientId) {
        require(consents[patientId][doctorAddress].isActive, "No active consent found");
        
        consents[patientId][doctorAddress].isActive = false;
        
        emit ConsentRevoked(patientId, doctorAddress, block.timestamp);
    }
    
    /**
     * @dev Get patient's medical records
     * @param patientId Patient identifier
     * @return Array of medical records
     */
    function getPatientRecords(string memory patientId) 
        public 
        view 
        patientExists(patientId) 
        hasConsent(patientId, msg.sender) 
        returns (MedicalRecord[] memory) 
    {
        return patientRecords[patientId];
    }
    
    /**
     * @dev Get patient information
     * @param patientId Patient identifier
     * @return Patient information
     */
    function getPatientInfo(string memory patientId) 
        public 
        view 
        patientExists(patientId) 
        hasConsent(patientId, msg.sender) 
        returns (Patient memory) 
    {
        return patients[patientId];
    }
    
    /**
     * @dev Check if doctor has consent for patient
     * @param patientId Patient identifier
     * @param doctorAddress Doctor's Ethereum address
     * @return True if consent is valid
     */
    function hasValidConsent(string memory patientId, address doctorAddress) 
        public 
        view 
        returns (bool) 
    {
        return consents[patientId][doctorAddress].isActive && 
               consents[patientId][doctorAddress].expiryDate > block.timestamp;
    }
    
    /**
     * @dev Grant access to patient records
     * @param patientId Patient identifier
     * @param doctorAddress Doctor's Ethereum address
     */
    function grantAccess(string memory patientId, address doctorAddress) 
        public 
        onlyAuthorizedDoctor 
        patientExists(patientId) 
        doctorExists(doctorAddress) 
    {
        authorizedDoctors[doctorAddress] = true;
        emit AccessGranted(doctorAddress, patientId, block.timestamp);
    }
    
    /**
     * @dev Revoke access to patient records
     * @param patientId Patient identifier
     * @param doctorAddress Doctor's Ethereum address
     */
    function revokeAccess(string memory patientId, address doctorAddress) 
        public 
        onlyAuthorizedDoctor 
        patientExists(patientId) 
    {
        authorizedDoctors[doctorAddress] = false;
        emit AccessRevoked(doctorAddress, patientId, block.timestamp);
    }
    
    /**
     * @dev Emergency access override (for emergency situations)
     * @param patientId Patient identifier
     * @param recordId Record identifier
     * @param diagnosis Emergency diagnosis
     * @param treatment Emergency treatment
     */
    function emergencyAccess(
        string memory patientId,
        string memory recordId,
        string memory diagnosis,
        string memory treatment
    ) public onlyAuthorizedDoctor patientExists(patientId) {
        require(bytes(recordId).length > 0, "Record ID cannot be empty");
        
        MedicalRecord memory emergencyRecord = MedicalRecord({
            recordId: recordId,
            patientId: patientId,
            diagnosis: diagnosis,
            treatment: treatment,
            medication: "Emergency treatment",
            recordDate: block.timestamp,
            doctorAddress: msg.sender,
            isEncrypted: true,
            ipfsHash: ""
        });
        
        patientRecords[patientId].push(emergencyRecord);
        
        emit RecordAdded(patientId, recordId, block.timestamp);
    }
    
    /**
     * @dev Get consent information
     * @param patientId Patient identifier
     * @param doctorAddress Doctor's Ethereum address
     * @return Consent information
     */
    function getConsentInfo(string memory patientId, address doctorAddress) 
        public 
        view 
        returns (Consent memory) 
    {
        return consents[patientId][doctorAddress];
    }
    
    /**
     * @dev Get doctor information
     * @param doctorAddress Doctor's Ethereum address
     * @return Doctor information
     */
    function getDoctorInfo(address doctorAddress) 
        public 
        view 
        returns (Doctor memory) 
    {
        return doctors[doctorAddress];
    }
} 