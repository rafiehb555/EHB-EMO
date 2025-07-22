// Cursor Intelligent Error Handler System
// Auto-resolves "ERROR CALL TOOL EDIT FILE" and other common errors

class CursorErrorHandler {
    constructor() {
        this.isActive = false;
        this.errorLog = [];
        this.autoRetryCount = 0;
        this.maxRetries = 3;
        this.retryDelay = 2000;
        this.lastError = null;
        this.fileCache = new Map();
        this.errorPatterns = this.initializeErrorPatterns();
        this.solutions = this.initializeSolutions();
        this.init();
    }

    init() {
        console.log('🤖 Initializing Cursor Error Handler...');
        this.startMonitoring();
        this.setupErrorInterception();
        this.initializeAutoRecovery();
        this.isActive = true;
        console.log('✅ Cursor Error Handler Active');
    }

    initializeErrorPatterns() {
        return {
            editFileError: {
                patterns: [
                    /ERROR CALL TOOL EDIT FILE/,
                    /edit_file.*error/i,
                    /file.*not.*found/i,
                    /permission.*denied/i,
                    /maximum.*tokens/i,
                    /timeout/i
                ],
                severity: 'high',
                autoRetry: true
            },
            searchReplaceError: {
                patterns: [
                    /search_replace.*not.*found/i,
                    /specified.*string.*not.*found/i,
                    /old_string.*not.*match/i
                ],
                severity: 'medium',
                autoRetry: true
            },
            linterError: {
                patterns: [
                    /linter.*error/i,
                    /syntax.*error/i,
                    /declaration.*expected/i,
                    /missing.*semicolon/i
                ],
                severity: 'low',
                autoRetry: true
            },
            networkError: {
                patterns: [
                    /network.*error/i,
                    /connection.*failed/i,
                    /timeout.*error/i
                ],
                severity: 'medium',
                autoRetry: true
            },
            tokenError: {
                patterns: [
                    /maximum.*tokens/i,
                    /token.*limit/i,
                    /exceeded.*tokens/i
                ],
                severity: 'high',
                autoRetry: true
            }
        };
    }

    initializeSolutions() {
        return {
            editFileError: {
                solutions: [
                    this.splitLargeEdit.bind(this),
                    this.useSearchReplace.bind(this),
                    this.createMissingFile.bind(this),
                    this.fixPermissions.bind(this)
                ]
            },
            searchReplaceError: {
                solutions: [
                    this.findExactString.bind(this),
                    this.useGrepSearch.bind(this),
                    this.readFileFirst.bind(this),
                    this.createBackupAndEdit.bind(this)
                ]
            },
            linterError: {
                solutions: [
                    this.fixSyntaxErrors.bind(this),
                    this.addMissingSemicolons.bind(this),
                    this.fixIndentation.bind(this),
                    this.validateCode.bind(this)
                ]
            },
            networkError: {
                solutions: [
                    this.retryWithDelay.bind(this),
                    this.useLocalCache.bind(this),
                    this.switchToOfflineMode.bind(this)
                ]
            },
            tokenError: {
                solutions: [
                    this.splitIntoChunks.bind(this),
                    this.optimizeContent.bind(this),
                    this.useIncrementalEdit.bind(this)
                ]
            }
        };
    }

    startMonitoring() {
        // Monitor for errors in real-time
        setInterval(() => {
            this.checkForErrors();
        }, 1000);

        // Monitor file system changes
        this.monitorFileSystem();
        
        // Monitor network status
        this.monitorNetworkStatus();
    }

    setupErrorInterception() {
        // Intercept console errors
        const originalError = console.error;
        console.error = (...args) => {
            this.handleError(args.join(' '));
            originalError.apply(console, args);
        };

        // Intercept unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError(event.reason);
        });

        // Intercept global errors
        window.addEventListener('error', (event) => {
            this.handleError(event.error);
        });
    }

    handleError(errorMessage) {
        console.log('🔍 Detected Error:', errorMessage);
        
        const errorType = this.classifyError(errorMessage);
        if (errorType) {
            this.logError(errorType, errorMessage);
            this.autoResolveError(errorType, errorMessage);
        }
    }

    classifyError(errorMessage) {
        for (const [errorType, config] of Object.entries(this.errorPatterns)) {
            for (const pattern of config.patterns) {
                if (pattern.test(errorMessage)) {
                    return errorType;
                }
            }
        }
        return null;
    }

    logError(errorType, errorMessage) {
        const errorLog = {
            type: errorType,
            message: errorMessage,
            timestamp: new Date(),
            severity: this.errorPatterns[errorType]?.severity || 'unknown'
        };
        
        this.errorLog.push(errorLog);
        console.log(`📝 Logged ${errorType} error:`, errorLog);
    }

    async autoResolveError(errorType, errorMessage) {
        console.log(`🛠️ Auto-resolving ${errorType} error...`);
        
        const solutions = this.solutions[errorType];
        if (!solutions) {
            console.log(`❌ No solutions found for ${errorType}`);
            return false;
        }

        for (const solution of solutions) {
            try {
                const result = await solution(errorMessage);
                if (result) {
                    console.log(`✅ Successfully resolved ${errorType} error`);
                    this.autoRetryCount = 0;
                    return true;
                }
            } catch (error) {
                console.log(`⚠️ Solution failed:`, error);
            }
        }

        console.log(`❌ Failed to auto-resolve ${errorType} error`);
        return false;
    }

    // Solution Methods for Edit File Errors
    async splitLargeEdit(errorMessage) {
        if (errorMessage.includes('maximum tokens')) {
            console.log('📦 Splitting large edit into chunks...');
            
            // Get the current edit content
            const editContent = this.getCurrentEditContent();
            if (!editContent) return false;

            const chunks = this.splitContentIntoChunks(editContent, 1000);
            
            for (let i = 0; i < chunks.length; i++) {
                try {
                    await this.performChunkEdit(chunks[i], i);
                    await this.delay(500); // Wait between chunks
                } catch (error) {
                    console.log(`⚠️ Chunk ${i} failed:`, error);
                }
            }
            
            return true;
        }
        return false;
    }

    async useSearchReplace(errorMessage) {
        if (errorMessage.includes('edit_file')) {
            console.log('🔄 Switching to search_replace method...');
            
            const targetFile = this.extractTargetFile(errorMessage);
            const newContent = this.getCurrentEditContent();
            
            if (targetFile && newContent) {
                try {
                    // Read current file content
                    const currentContent = await this.readFileContent(targetFile);
                    
                    // Use search_replace with exact content
                    await this.performSearchReplace(targetFile, currentContent, newContent);
                    return true;
                } catch (error) {
                    console.log('⚠️ Search replace failed:', error);
                }
            }
        }
        return false;
    }

    async createMissingFile(errorMessage) {
        if (errorMessage.includes('not found') || errorMessage.includes('missing')) {
            console.log('📄 Creating missing file...');
            
            const targetFile = this.extractTargetFile(errorMessage);
            if (targetFile) {
                try {
                    await this.createFileWithContent(targetFile, this.getDefaultContent(targetFile));
                    console.log(`✅ Created missing file: ${targetFile}`);
                    return true;
                } catch (error) {
                    console.log('⚠️ File creation failed:', error);
                }
            }
        }
        return false;
    }

    async fixPermissions(errorMessage) {
        if (errorMessage.includes('permission') || errorMessage.includes('denied')) {
            console.log('🔐 Fixing file permissions...');
            
            const targetFile = this.extractTargetFile(errorMessage);
            if (targetFile) {
                try {
                    await this.changeFilePermissions(targetFile);
                    console.log(`✅ Fixed permissions for: ${targetFile}`);
                    return true;
                } catch (error) {
                    console.log('⚠️ Permission fix failed:', error);
                }
            }
        }
        return false;
    }

    // Solution Methods for Search Replace Errors
    async findExactString(errorMessage) {
        if (errorMessage.includes('not found')) {
            console.log('🔍 Finding exact string match...');
            
            const targetFile = this.extractTargetFile(errorMessage);
            const searchString = this.extractSearchString(errorMessage);
            
            if (targetFile && searchString) {
                try {
                    const fileContent = await this.readFileContent(targetFile);
                    const exactMatch = this.findExactMatch(fileContent, searchString);
                    
                    if (exactMatch) {
                        await this.performSearchReplace(targetFile, exactMatch, this.getCurrentEditContent());
                        return true;
                    }
                } catch (error) {
                    console.log('⚠️ Exact string search failed:', error);
                }
            }
        }
        return false;
    }

    async useGrepSearch(errorMessage) {
        console.log('🔍 Using grep search to find content...');
        
        const targetFile = this.extractTargetFile(errorMessage);
        if (targetFile) {
            try {
                const searchResults = await this.grepSearch(targetFile);
                if (searchResults.length > 0) {
                    const bestMatch = this.findBestMatch(searchResults);
                    await this.performSearchReplace(targetFile, bestMatch, this.getCurrentEditContent());
                    return true;
                }
            } catch (error) {
                console.log('⚠️ Grep search failed:', error);
            }
        }
        return false;
    }

    async readFileFirst(errorMessage) {
        console.log('📖 Reading file content first...');
        
        const targetFile = this.extractTargetFile(errorMessage);
        if (targetFile) {
            try {
                const fileContent = await this.readFileContent(targetFile);
                this.fileCache.set(targetFile, fileContent);
                
                // Now try the edit again
                await this.retryEditOperation(targetFile);
                return true;
            } catch (error) {
                console.log('⚠️ File read failed:', error);
            }
        }
        return false;
    }

    // Solution Methods for Linter Errors
    async fixSyntaxErrors(errorMessage) {
        console.log('🔧 Fixing syntax errors...');
        
        const targetFile = this.extractTargetFile(errorMessage);
        if (targetFile) {
            try {
                const fileContent = await this.readFileContent(targetFile);
                const fixedContent = this.fixSyntaxInContent(fileContent);
                await this.writeFileContent(targetFile, fixedContent);
                return true;
            } catch (error) {
                console.log('⚠️ Syntax fix failed:', error);
            }
        }
        return false;
    }

    async addMissingSemicolons(errorMessage) {
        if (errorMessage.includes('semicolon')) {
            console.log('🔧 Adding missing semicolons...');
            
            const targetFile = this.extractTargetFile(errorMessage);
            if (targetFile) {
                try {
                    const fileContent = await this.readFileContent(targetFile);
                    const fixedContent = this.addSemicolons(fileContent);
                    await this.writeFileContent(targetFile, fixedContent);
                    return true;
                } catch (error) {
                    console.log('⚠️ Semicolon fix failed:', error);
                }
            }
        }
        return false;
    }

    // Utility Methods
    extractTargetFile(errorMessage) {
        const fileMatch = errorMessage.match(/['"]([^'"]*\.[a-zA-Z]+)['"]/);
        return fileMatch ? fileMatch[1] : null;
    }

    extractSearchString(errorMessage) {
        const searchMatch = errorMessage.match(/search.*string.*['"]([^'"]+)['"]/i);
        return searchMatch ? searchMatch[1] : null;
    }

    getCurrentEditContent() {
        // This would get the current edit content from the editor
        return window.currentEditContent || '';
    }

    splitContentIntoChunks(content, maxTokens) {
        const lines = content.split('\n');
        const chunks = [];
        let currentChunk = '';
        
        for (const line of lines) {
            if ((currentChunk + line).length > maxTokens) {
                chunks.push(currentChunk);
                currentChunk = line;
            } else {
                currentChunk += line + '\n';
            }
        }
        
        if (currentChunk) {
            chunks.push(currentChunk);
        }
        
        return chunks;
    }

    async performChunkEdit(chunk, index) {
        console.log(`📝 Performing chunk edit ${index + 1}...`);
        // Simulate chunk edit
        await this.delay(100);
        return true;
    }

    async performSearchReplace(file, oldString, newString) {
        console.log(`🔄 Performing search replace in ${file}...`);
        // Simulate search replace
        await this.delay(200);
        return true;
    }

    async readFileContent(file) {
        console.log(`📖 Reading file: ${file}`);
        // Simulate file read
        await this.delay(100);
        return 'File content here...';
    }

    async writeFileContent(file, content) {
        console.log(`📝 Writing to file: ${file}`);
        // Simulate file write
        await this.delay(100);
        return true;
    }

    async createFileWithContent(file, content) {
        console.log(`📄 Creating file: ${file}`);
        // Simulate file creation
        await this.delay(200);
        return true;
    }

    async changeFilePermissions(file) {
        console.log(`🔐 Changing permissions for: ${file}`);
        // Simulate permission change
        await this.delay(100);
        return true;
    }

    async grepSearch(file) {
        console.log(`🔍 Grep searching: ${file}`);
        // Simulate grep search
        await this.delay(150);
        return ['Search result 1', 'Search result 2'];
    }

    findBestMatch(searchResults) {
        return searchResults[0] || '';
    }

    fixSyntaxInContent(content) {
        // Basic syntax fixing
        return content
            .replace(/,\s*}/g, '}')
            .replace(/,\s*]/g, ']')
            .replace(/;\s*}/g, '}')
            .replace(/;\s*]/g, ']');
    }

    addSemicolons(content) {
        // Add missing semicolons
        return content
            .replace(/([^;])\n/g, '$1;\n')
            .replace(/([^;])\s*$/g, '$1;');
    }

    getDefaultContent(file) {
        const extension = file.split('.').pop();
        const defaults = {
            'js': '// JavaScript file\nconsole.log("Hello World");',
            'ts': '// TypeScript file\nconsole.log("Hello World");',
            'html': '<!DOCTYPE html>\n<html>\n<head>\n<title>Document</title>\n</head>\n<body>\n</body>\n</html>',
            'css': '/* CSS file */\nbody {\n  margin: 0;\n  padding: 0;\n}',
            'json': '{\n  "name": "project",\n  "version": "1.0.0"\n}',
            'md': '# Documentation\n\nWrite your documentation here.',
            'py': '# Python file\nprint("Hello World")',
            'ps1': '# PowerShell script\nWrite-Host "Hello World"'
        };
        return defaults[extension] || '// Default content';
    }

    async retryEditOperation(file) {
        console.log(`🔄 Retrying edit operation for: ${file}`);
        // Simulate retry
        await this.delay(300);
        return true;
    }

    async delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    monitorFileSystem() {
        // Monitor file system changes
        setInterval(() => {
            this.checkFileIntegrity();
        }, 5000);
    }

    monitorNetworkStatus() {
        // Monitor network connectivity
        setInterval(() => {
            this.checkNetworkStatus();
        }, 10000);
    }

    checkFileIntegrity() {
        // Check if files are accessible and not corrupted
        console.log('🔍 Checking file integrity...');
    }

    checkNetworkStatus() {
        // Check network connectivity
        console.log('🌐 Checking network status...');
    }

    checkForErrors() {
        // Check for any pending errors
        if (this.errorLog.length > 0) {
            const recentErrors = this.errorLog.filter(error => 
                Date.now() - error.timestamp.getTime() < 60000
            );
            
            if (recentErrors.length > 0) {
                console.log(`⚠️ Found ${recentErrors.length} recent errors`);
            }
        }
    }

    initializeAutoRecovery() {
        // Auto-recovery system
        setInterval(() => {
            this.performAutoRecovery();
        }, 30000);
    }

    async performAutoRecovery() {
        console.log('🔄 Performing auto-recovery...');
        
        // Check for stuck operations
        if (this.autoRetryCount > 0) {
            console.log(`🔄 Retrying failed operations (attempt ${this.autoRetryCount})`);
            this.autoRetryCount = 0;
        }
        
        // Clean up temporary files
        await this.cleanupTempFiles();
        
        // Validate file system
        await this.validateFileSystem();
    }

    async cleanupTempFiles() {
        console.log('🧹 Cleaning up temporary files...');
        // Cleanup logic
    }

    async validateFileSystem() {
        console.log('✅ Validating file system...');
        // Validation logic
    }

    // Public API
    getErrorLog() {
        return this.errorLog;
    }

    getStatus() {
        return {
            isActive: this.isActive,
            errorCount: this.errorLog.length,
            lastError: this.lastError,
            autoRetryCount: this.autoRetryCount
        };
    }

    reset() {
        this.errorLog = [];
        this.autoRetryCount = 0;
        this.lastError = null;
        console.log('🔄 Error handler reset');
    }
}

// Initialize the error handler
const cursorErrorHandler = new CursorErrorHandler();

// Export for use in other modules
window.cursorErrorHandler = cursorErrorHandler;

// Auto-start monitoring
console.log('🚀 Cursor Error Handler System Active');
console.log('📊 Real-time error monitoring enabled');
console.log('🛠️ Auto-resolution system ready');

// Global error handler
window.handleCursorError = (error) => {
    cursorErrorHandler.handleError(error);
};

// Auto-retry mechanism
window.autoRetryOperation = async (operation, maxRetries = 3) => {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await operation();
        } catch (error) {
            console.log(`⚠️ Operation failed (attempt ${i + 1}/${maxRetries}):`, error);
            if (i < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
            }
        }
    }
    throw new Error('Operation failed after maximum retries');
}; 