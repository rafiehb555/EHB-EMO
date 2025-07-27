#!/usr/bin/env node
/**
 * 🌐 Website Cloning System
 * High-level tool to clone any website, extract code, and integrate with your project
 */

const fs = require('fs').promises;
const path = require('path');
const puppeteer = require('puppeteer');
const axios = require('axios');
const cheerio = require('cheerio');
const { JSDOM } = require('jsdom');

class WebsiteCloningSystem {
    constructor() {
        this.browser = null;
        this.page = null;
        this.outputDir = 'cloned_website';
        this.assets = {
            css: [],
            js: [],
            images: [],
            fonts: [],
            others: []
        };
    }

    /**
     * Initialize the cloning system
     */
    async initialize() {
        console.log('🚀 Initializing Website Cloning System...');

        this.browser = await puppeteer.launch({
            headless: 'new',
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        });

        this.page = await this.browser.newPage();

        // Set user agent
        await this.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

        // Set viewport
        await this.page.setViewport({ width: 1920, height: 1080 });

        console.log('✅ System initialized successfully');
    }

    /**
     * Clone a website completely
     */
    async cloneWebsite(url, options = {}) {
        console.log(`🌐 Starting to clone: ${url}`);

        try {
            // Set output directory
            this.outputDir = options.outputDir || `cloned_${this.sanitizeFilename(new URL(url).hostname)}`;

            // Create output directory
            await this.createDirectory(this.outputDir);

            // Navigate to the website
            console.log('📄 Loading website...');
            await this.page.goto(url, {
                waitUntil: 'networkidle2',
                timeout: 60000
            });

            // Wait for dynamic content
            await new Promise(resolve => setTimeout(resolve, 3000));

            // Extract website data
            const websiteData = await this.extractWebsiteData(url);

            // Download all assets
            await this.downloadAssets(url);

            // Generate HTML file
            await this.generateHTML(websiteData);

            // Extract and save CSS
            await this.extractAndSaveCSS();

            // Extract and save JavaScript
            await this.extractAndSaveJS();

            // Create analysis report
            await this.createAnalysisReport(url, websiteData);

            // Create integration files
            await this.createIntegrationFiles(websiteData);

            console.log(`🎉 Website cloned successfully to: ${this.outputDir}`);
            return {
                success: true,
                outputDir: this.outputDir,
                data: websiteData
            };

        } catch (error) {
            console.error('❌ Error cloning website:', error.message);
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Extract comprehensive website data
     */
    async extractWebsiteData(url) {
        console.log('🔍 Extracting website data...');

        const data = await this.page.evaluate((baseUrl) => {
            const data = {
                title: document.title,
                description: '',
                keywords: '',
                favicon: '',
                language: document.documentElement.lang || 'en',
                charset: document.charset || 'UTF-8',
                viewport: '',
                canonicalUrl: baseUrl,
                openGraph: {},
                twitterCard: {},
                structuredData: [],
                stylesheets: [],
                scripts: [],
                images: [],
                links: [],
                forms: [],
                tables: [],
                navigation: [],
                footer: [],
                sidebar: [],
                content: [],
                metadata: {},
                technologies: [],
                performance: {},
                accessibility: {},
                seo: {}
            };

            // Extract meta tags
            document.querySelectorAll('meta').forEach(meta => {
                const name = meta.getAttribute('name') || meta.getAttribute('property');
                const content = meta.getAttribute('content');

                if (name && content) {
                    if (name === 'description') data.description = content;
                    else if (name === 'keywords') data.keywords = content;
                    else if (name === 'viewport') data.viewport = content;
                    else if (name.startsWith('og:')) data.openGraph[name] = content;
                    else if (name.startsWith('twitter:')) data.twitterCard[name] = content;
                    else data.metadata[name] = content;
                }
            });

            // Extract favicon
            const favicon = document.querySelector('link[rel*="icon"]');
            if (favicon) data.favicon = favicon.href;

            // Extract stylesheets
            document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
                data.stylesheets.push({
                    href: link.href,
                    media: link.media || 'all',
                    type: link.type || 'text/css'
                });
            });

            // Extract scripts
            document.querySelectorAll('script[src]').forEach(script => {
                data.scripts.push({
                    src: script.src,
                    type: script.type || 'text/javascript',
                    async: script.async,
                    defer: script.defer
                });
            });

            // Extract images
            document.querySelectorAll('img').forEach(img => {
                data.images.push({
                    src: img.src,
                    alt: img.alt || '',
                    width: img.width || '',
                    height: img.height || '',
                    loading: img.loading || '',
                    srcset: img.srcset || ''
                });
            });

            // Extract links
            document.querySelectorAll('a[href]').forEach(link => {
                data.links.push({
                    href: link.href,
                    text: link.textContent.trim(),
                    title: link.title || '',
                    target: link.target || '',
                    rel: link.rel || ''
                });
            });

            // Extract forms
            document.querySelectorAll('form').forEach(form => {
                const fields = [];
                form.querySelectorAll('input, select, textarea').forEach(field => {
                    fields.push({
                        type: field.type || field.tagName.toLowerCase(),
                        name: field.name || '',
                        id: field.id || '',
                        placeholder: field.placeholder || '',
                        required: field.required || false,
                        value: field.value || ''
                    });
                });

                data.forms.push({
                    action: form.action || '',
                    method: form.method || 'GET',
                    enctype: form.enctype || '',
                    fields: fields
                });
            });

            // Extract navigation
            document.querySelectorAll('nav, .nav, .navigation, .menu').forEach(nav => {
                const links = [];
                nav.querySelectorAll('a').forEach(link => {
                    links.push({
                        href: link.href,
                        text: link.textContent.trim()
                    });
                });
                data.navigation.push({
                    class: nav.className,
                    id: nav.id,
                    links: links
                });
            });

            // Extract structured data
            document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
                try {
                    data.structuredData.push(JSON.parse(script.textContent));
                } catch (e) {
                    // Ignore invalid JSON
                }
            });

            // Extract main content
            const contentSelectors = [
                'main', '.main', '#main',
                'article', '.article',
                '.content', '#content',
                '.container', '.wrapper'
            ];

            contentSelectors.forEach(selector => {
                const element = document.querySelector(selector);
                if (element) {
                    data.content.push({
                        selector: selector,
                        html: element.innerHTML,
                        text: element.textContent.trim()
                    });
                }
            });

            // Detect technologies
            const techIndicators = {
                'React': () => window.React || document.querySelector('[data-reactroot]') || document.querySelector('*[data-react-class]'),
                'Vue.js': () => window.Vue || document.querySelector('[data-v-]') || document.querySelector('*[v-]'),
                'Angular': () => window.angular || document.querySelector('[ng-app]') || document.querySelector('*[ng-]'),
                'jQuery': () => window.jQuery || window.$,
                'Bootstrap': () => document.querySelector('.container') || document.querySelector('.row') || document.querySelector('.col-'),
                'Tailwind CSS': () => document.querySelector('[class*="w-"]') || document.querySelector('[class*="h-"]'),
                'Font Awesome': () => document.querySelector('.fa') || document.querySelector('.fas') || document.querySelector('.far'),
                'Google Analytics': () => window.gtag || window.ga || document.querySelector('script[src*="google-analytics"]'),
                'Google Tag Manager': () => window.dataLayer || document.querySelector('script[src*="googletagmanager"]')
            };

            Object.keys(techIndicators).forEach(tech => {
                try {
                    if (techIndicators[tech]()) {
                        data.technologies.push(tech);
                    }
                } catch (e) {
                    // Ignore errors
                }
            });

            return data;
        }, url);

        // Get performance metrics
        const performanceMetrics = await this.page.metrics();
        data.performance = performanceMetrics;

        // Get accessibility info
        data.accessibility = await this.getAccessibilityInfo();

        return data;
    }

    /**
     * Download all website assets
     */
    async downloadAssets(baseUrl) {
        console.log('📦 Downloading assets...');

        // Create asset directories
        await this.createDirectory(path.join(this.outputDir, 'assets', 'css'));
        await this.createDirectory(path.join(this.outputDir, 'assets', 'js'));
        await this.createDirectory(path.join(this.outputDir, 'assets', 'images'));
        await this.createDirectory(path.join(this.outputDir, 'assets', 'fonts'));

        // Get all resources
        const resources = await this.page.evaluate(() => {
            const resources = [];

            // CSS files
            document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
                resources.push({ type: 'css', url: link.href });
            });

            // JS files
            document.querySelectorAll('script[src]').forEach(script => {
                resources.push({ type: 'js', url: script.src });
            });

            // Images
            document.querySelectorAll('img[src]').forEach(img => {
                resources.push({ type: 'image', url: img.src });
            });

            // Background images
            document.querySelectorAll('*').forEach(el => {
                const style = window.getComputedStyle(el);
                const bgImage = style.backgroundImage;
                if (bgImage && bgImage !== 'none') {
                    const match = bgImage.match(/url\("?([^"]*)"?\)/);
                    if (match) {
                        resources.push({ type: 'image', url: match[1] });
                    }
                }
            });

            return resources;
        });

        // Download each resource
        for (const resource of resources) {
            try {
                await this.downloadResource(resource, baseUrl);
            } catch (error) {
                console.warn(`⚠️  Failed to download ${resource.url}:`, error.message);
            }
        }
    }

    /**
     * Download a single resource
     */
    async downloadResource(resource, baseUrl) {
        try {
            // Resolve URL
            const fullUrl = new URL(resource.url, baseUrl).href;

            // Download the resource
            const response = await axios.get(fullUrl, {
                responseType: 'arraybuffer',
                timeout: 30000,
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            });

            // Determine file path
            const urlPath = new URL(fullUrl).pathname;
            const filename = path.basename(urlPath) || `file_${Date.now()}`;
            const extension = path.extname(filename) || this.getExtensionFromType(resource.type);
            const finalFilename = filename.includes('.') ? filename : `${filename}${extension}`;

            let assetPath;
            switch (resource.type) {
                case 'css':
                    assetPath = path.join(this.outputDir, 'assets', 'css', finalFilename);
                    break;
                case 'js':
                    assetPath = path.join(this.outputDir, 'assets', 'js', finalFilename);
                    break;
                case 'image':
                    assetPath = path.join(this.outputDir, 'assets', 'images', finalFilename);
                    break;
                default:
                    assetPath = path.join(this.outputDir, 'assets', finalFilename);
            }

            // Save the file
            await fs.writeFile(assetPath, response.data);

            // Track the asset
            this.assets[resource.type === 'image' ? 'images' : resource.type].push({
                original: fullUrl,
                local: path.relative(this.outputDir, assetPath),
                filename: finalFilename
            });

        } catch (error) {
            throw new Error(`Failed to download ${resource.url}: ${error.message}`);
        }
    }

    /**
     * Generate HTML file with local assets
     */
    async generateHTML(data) {
        console.log('📝 Generating HTML file...');

        // Get the full HTML
        const htmlContent = await this.page.content();

        // Parse with cheerio for manipulation
        const $ = cheerio.load(htmlContent);

        // Update asset paths to local paths
        this.updateAssetPaths($);

        // Add our custom scripts and styles
        this.addCustomEnhancements($, data);

        // Save the HTML file
        const finalHtml = $.html();
        await fs.writeFile(path.join(this.outputDir, 'index.html'), finalHtml, 'utf8');
    }

    /**
     * Update asset paths to local paths
     */
    updateAssetPaths($) {
        // Update CSS links
        $('link[rel="stylesheet"]').each((i, el) => {
            const href = $(el).attr('href');
            const localAsset = this.assets.css.find(asset => asset.original === href);
            if (localAsset) {
                $(el).attr('href', 'assets/css/' + localAsset.filename);
            }
        });

        // Update script sources
        $('script[src]').each((i, el) => {
            const src = $(el).attr('src');
            const localAsset = this.assets.js.find(asset => asset.original === src);
            if (localAsset) {
                $(el).attr('src', 'assets/js/' + localAsset.filename);
            }
        });

        // Update image sources
        $('img[src]').each((i, el) => {
            const src = $(el).attr('src');
            const localAsset = this.assets.images.find(asset => asset.original === src);
            if (localAsset) {
                $(el).attr('src', 'assets/images/' + localAsset.filename);
            }
        });
    }

    /**
     * Add custom enhancements to the cloned website
     */
    addCustomEnhancements($, data) {
        // Add a banner indicating this is a cloned website
        const banner = `
        <div id="cloned-banner" style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px;
            text-align: center;
            z-index: 9999;
            font-family: Arial, sans-serif;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        ">
            🌐 This is a cloned website for development purposes. Original: ${data.canonicalUrl}
            <button onclick="document.getElementById('cloned-banner').style.display='none'" style="
                margin-left: 20px;
                background: white;
                color: #333;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                cursor: pointer;
            ">Hide</button>
        </div>
        `;

        $('body').prepend(banner);

        // Add custom CSS to adjust for banner
        $('head').append(`
        <style>
            body { margin-top: 60px !important; }
            #cloned-banner + * { margin-top: 0 !important; }
        </style>
        `);

        // Add development tools
        const devTools = `
        <script>
            // Cloned website development tools
            console.log('🌐 Cloned Website Loaded');
            console.log('Original URL:', '${data.canonicalUrl}');
            console.log('Technologies detected:', ${JSON.stringify(data.technologies)});

            // Add right-click menu for development
            document.addEventListener('contextmenu', function(e) {
                if (e.ctrlKey) {
                    e.preventDefault();
                    console.log('Element:', e.target);
                    console.log('Classes:', e.target.className);
                    console.log('ID:', e.target.id);
                    alert('Element info logged to console');
                }
            });
        </script>
        `;

        $('body').append(devTools);
    }

    /**
     * Extract and save CSS
     */
    async extractAndSaveCSS() {
        console.log('🎨 Extracting CSS...');

        // Get all computed styles
        const allStyles = await this.page.evaluate(() => {
            const styles = [];

            // Get all stylesheets
            for (let i = 0; i < document.styleSheets.length; i++) {
                try {
                    const sheet = document.styleSheets[i];
                    const rules = sheet.cssRules || sheet.rules;

                    for (let j = 0; j < rules.length; j++) {
                        styles.push(rules[j].cssText);
                    }
                } catch (e) {
                    // Skip if stylesheet is not accessible (CORS)
                }
            }

            return styles.join('\n');
        });

        // Save extracted CSS
        await fs.writeFile(
            path.join(this.outputDir, 'assets', 'css', 'extracted-styles.css'),
            allStyles,
            'utf8'
        );
    }

    /**
     * Extract and save JavaScript
     */
    async extractAndSaveJS() {
        console.log('⚙️ Extracting JavaScript...');

        // Get all inline scripts
        const inlineScripts = await this.page.evaluate(() => {
            const scripts = [];
            document.querySelectorAll('script:not([src])').forEach(script => {
                if (script.textContent.trim()) {
                    scripts.push(script.textContent);
                }
            });
            return scripts;
        });

        // Save inline scripts
        if (inlineScripts.length > 0) {
            const combinedScript = inlineScripts.join('\n\n/* ========== Next Script ========== */\n\n');
            await fs.writeFile(
                path.join(this.outputDir, 'assets', 'js', 'inline-scripts.js'),
                combinedScript,
                'utf8'
            );
        }
    }

    /**
     * Create analysis report
     */
    async createAnalysisReport(url, data) {
        console.log('📊 Creating analysis report...');

        const report = {
            analysisDate: new Date().toISOString(),
            originalUrl: url,
            clonedAt: new Date().toLocaleString(),
            website: {
                title: data.title,
                description: data.description,
                language: data.language,
                technologies: data.technologies
            },
            assets: {
                totalStylesheets: data.stylesheets.length,
                totalScripts: data.scripts.length,
                totalImages: data.images.length,
                totalLinks: data.links.length,
                totalForms: data.forms.length
            },
            performance: data.performance,
            seo: {
                hasTitle: !!data.title,
                hasDescription: !!data.description,
                hasKeywords: !!data.keywords,
                hasFavicon: !!data.favicon,
                hasViewport: !!data.viewport,
                hasOpenGraph: Object.keys(data.openGraph).length > 0,
                hasTwitterCard: Object.keys(data.twitterCard).length > 0,
                hasStructuredData: data.structuredData.length > 0
            },
            accessibility: data.accessibility,
            downloadedAssets: this.assets,
            recommendations: this.generateRecommendations(data)
        };

        await fs.writeFile(
            path.join(this.outputDir, 'analysis-report.json'),
            JSON.stringify(report, null, 2),
            'utf8'
        );

        // Create human-readable report
        const htmlReport = this.createHTMLReport(report);
        await fs.writeFile(
            path.join(this.outputDir, 'analysis-report.html'),
            htmlReport,
            'utf8'
        );
    }

    /**
     * Create integration files for different frameworks
     */
    async createIntegrationFiles(data) {
        console.log('🔧 Creating integration files...');

        // Create React component
        await this.createReactComponent(data);

        // Create Vue component
        await this.createVueComponent(data);

        // Create configuration files
        await this.createConfigFiles(data);

        // Create README
        await this.createREADME(data);
    }

    /**
     * Create React component from cloned website
     */
    async createReactComponent(data) {
        const componentCode = `
import React from 'react';
import './ClonedWebsite.css';

const ClonedWebsite = () => {
    return (
        <div className="cloned-website">
            <h1>${data.title}</h1>
            <p>${data.description}</p>

            {/* Navigation */}
            ${data.navigation.map(nav => `
            <nav className="${nav.class}">
                ${nav.links.map(link => `
                <a href="${link.href}">${link.text}</a>
                `).join('')}
            </nav>
            `).join('')}

            {/* Main Content */}
            <main>
                {/* Content will be populated from original website */}
                <p>This component was generated from: ${data.canonicalUrl}</p>
            </main>
        </div>
    );
};

export default ClonedWebsite;
        `;

        await fs.writeFile(
            path.join(this.outputDir, 'ClonedWebsite.jsx'),
            componentCode.trim(),
            'utf8'
        );
    }

    /**
     * Create Vue component from cloned website
     */
    async createVueComponent(data) {
        const componentCode = `
<template>
    <div class="cloned-website">
        <h1>${data.title}</h1>
        <p>${data.description}</p>

        <!-- Navigation -->
        <nav v-for="nav in navigation" :key="nav.id" :class="nav.class">
            <a v-for="link in nav.links" :key="link.href" :href="link.href">
                {{ link.text }}
            </a>
        </nav>

        <!-- Main Content -->
        <main>
            <p>This component was generated from: ${data.canonicalUrl}</p>
        </main>
    </div>
</template>

<script>
export default {
    name: 'ClonedWebsite',
    data() {
        return {
            navigation: ${JSON.stringify(data.navigation, null, 12)}
        };
    }
};
</script>

<style scoped>
/* Import the extracted styles */
@import './assets/css/extracted-styles.css';
</style>
        `;

        await fs.writeFile(
            path.join(this.outputDir, 'ClonedWebsite.vue'),
            componentCode.trim(),
            'utf8'
        );
    }

    /**
     * Create configuration files
     */
    async createConfigFiles(data) {
        // Package.json
        const packageJson = {
            name: `cloned-${this.sanitizeFilename(new URL(data.canonicalUrl).hostname)}`,
            version: "1.0.0",
            description: `Cloned website from ${data.canonicalUrl}`,
            main: "index.html",
            scripts: {
                start: "npx http-server . -p 3000",
                dev: "npx live-server .",
                build: "npm run build:css && npm run build:js",
                "build:css": "npx postcss assets/css/*.css -d dist/css",
                "build:js": "npx webpack assets/js/*.js -o dist/js"
            },
            dependencies: {
                "http-server": "^14.1.1",
                "live-server": "^1.2.2"
            },
            devDependencies: {
                "postcss": "^8.4.21",
                "webpack": "^5.75.0"
            },
            keywords: ["cloned", "website", data.title.toLowerCase()],
            author: "Website Cloning System",
            clonedFrom: data.canonicalUrl,
            clonedAt: new Date().toISOString(),
            technologies: data.technologies
        };

        await fs.writeFile(
            path.join(this.outputDir, 'package.json'),
            JSON.stringify(packageJson, null, 2),
            'utf8'
        );

        // Docker configuration
        const dockerfile = `
FROM nginx:alpine

# Copy cloned website files
COPY . /usr/share/nginx/html

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
        `;

        await fs.writeFile(
            path.join(this.outputDir, 'Dockerfile'),
            dockerfile.trim(),
            'utf8'
        );
    }

    /**
     * Create README file
     */
    async createREADME(data) {
        const readme = `
# Cloned Website: ${data.title}

This website was cloned from [${data.canonicalUrl}](${data.canonicalUrl}) using the Website Cloning System.

## 📋 Information

- **Original URL**: ${data.canonicalUrl}
- **Cloned Date**: ${new Date().toLocaleString()}
- **Title**: ${data.title}
- **Description**: ${data.description}
- **Language**: ${data.language}

## 🛠️ Technologies Detected

${data.technologies.map(tech => `- ${tech}`).join('\n')}

## 📦 Assets

- **Stylesheets**: ${data.stylesheets.length}
- **Scripts**: ${data.scripts.length}
- **Images**: ${data.images.length}
- **Forms**: ${data.forms.length}

## 🚀 Quick Start

### Option 1: Simple HTTP Server
\`\`\`bash
npm install
npm start
# Open http://localhost:3000
\`\`\`

### Option 2: Live Development Server
\`\`\`bash
npm run dev
# Opens browser automatically
\`\`\`

### Option 3: Docker
\`\`\`bash
docker build -t cloned-website .
docker run -p 8080:80 cloned-website
# Open http://localhost:8080
\`\`\`

## 📁 File Structure

\`\`\`
${this.outputDir}/
├── index.html              # Main HTML file
├── assets/
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   ├── images/             # Images
│   └── fonts/              # Fonts
├── ClonedWebsite.jsx       # React component
├── ClonedWebsite.vue       # Vue component
├── analysis-report.html    # Analysis report
├── analysis-report.json    # Raw analysis data
├── package.json           # Node.js configuration
├── Dockerfile             # Docker configuration
└── README.md              # This file
\`\`\`

## 🔧 Integration

### React Integration
\`\`\`jsx
import ClonedWebsite from './ClonedWebsite';

function App() {
    return <ClonedWebsite />;
}
\`\`\`

### Vue Integration
\`\`\`vue
<template>
    <ClonedWebsite />
</template>

<script>
import ClonedWebsite from './ClonedWebsite.vue';

export default {
    components: { ClonedWebsite }
};
</script>
\`\`\`

## 📊 Analysis Report

View the detailed analysis report at \`analysis-report.html\` for:
- Performance metrics
- SEO analysis
- Accessibility information
- Technology stack details
- Optimization recommendations

## ⚠️ Important Notes

1. This is a static clone of the original website
2. Dynamic functionality may not work without backend integration
3. Some assets might be missing due to CORS restrictions
4. External API calls will still point to the original endpoints
5. This clone is for development/learning purposes only

## 🔗 Original Website

Visit the original website: [${data.canonicalUrl}](${data.canonicalUrl})

---

Generated by Website Cloning System 🌐
        `;

        await fs.writeFile(
            path.join(this.outputDir, 'README.md'),
            readme.trim(),
            'utf8'
        );
    }

    /**
     * Helper methods
     */
    async createDirectory(dirPath) {
        try {
            await fs.mkdir(dirPath, { recursive: true });
        } catch (error) {
            if (error.code !== 'EEXIST') {
                throw error;
            }
        }
    }

    sanitizeFilename(filename) {
        return filename.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    }

    getExtensionFromType(type) {
        const extensions = {
            css: '.css',
            js: '.js',
            image: '.jpg'
        };
        return extensions[type] || '';
    }

    async getAccessibilityInfo() {
        return await this.page.evaluate(() => {
            const accessibility = {
                hasAltTexts: true,
                hasHeadings: document.querySelectorAll('h1, h2, h3, h4, h5, h6').length > 0,
                hasSkipLinks: document.querySelectorAll('a[href*="#"]').length > 0,
                hasAriaLabels: document.querySelectorAll('[aria-label]').length > 0,
                hasLandmarks: document.querySelectorAll('main, nav, header, footer, section, aside').length > 0
            };

            // Check alt texts
            document.querySelectorAll('img').forEach(img => {
                if (!img.alt || img.alt.trim() === '') {
                    accessibility.hasAltTexts = false;
                }
            });

            return accessibility;
        });
    }

    generateRecommendations(data) {
        const recommendations = [];

        if (!data.title) recommendations.push('Add a proper page title');
        if (!data.description) recommendations.push('Add a meta description');
        if (!data.viewport) recommendations.push('Add viewport meta tag for mobile responsiveness');
        if (!data.favicon) recommendations.push('Add a favicon');
        if (data.technologies.length === 0) recommendations.push('Consider using modern web frameworks');
        if (data.images.length > 50) recommendations.push('Optimize images for better performance');
        if (data.scripts.length > 20) recommendations.push('Consider bundling JavaScript files');

        return recommendations;
    }

    createHTMLReport(report) {
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Website Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        .header { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .good { color: green; }
        .bad { color: red; }
        .warning { color: orange; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #f4f4f4; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Website Analysis Report</h1>
        <p><strong>Original URL:</strong> ${report.originalUrl}</p>
        <p><strong>Analysis Date:</strong> ${report.analysisDate}</p>
    </div>

    <div class="section">
        <h2>Website Information</h2>
        <table>
            <tr><td>Title</td><td>${report.website.title}</td></tr>
            <tr><td>Description</td><td>${report.website.description}</td></tr>
            <tr><td>Language</td><td>${report.website.language}</td></tr>
            <tr><td>Technologies</td><td>${report.website.technologies.join(', ')}</td></tr>
        </table>
    </div>

    <div class="section">
        <h2>SEO Analysis</h2>
        <ul>
            <li class="${report.seo.hasTitle ? 'good' : 'bad'}">Title: ${report.seo.hasTitle ? '✓' : '✗'}</li>
            <li class="${report.seo.hasDescription ? 'good' : 'bad'}">Description: ${report.seo.hasDescription ? '✓' : '✗'}</li>
            <li class="${report.seo.hasKeywords ? 'good' : 'warning'}">Keywords: ${report.seo.hasKeywords ? '✓' : '✗'}</li>
            <li class="${report.seo.hasFavicon ? 'good' : 'warning'}">Favicon: ${report.seo.hasFavicon ? '✓' : '✗'}</li>
            <li class="${report.seo.hasViewport ? 'good' : 'bad'}">Viewport: ${report.seo.hasViewport ? '✓' : '✗'}</li>
        </ul>
    </div>

    <div class="section">
        <h2>Recommendations</h2>
        <ul>
            ${report.recommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ul>
    </div>
</body>
</html>
        `;
    }

    /**
     * Cleanup resources
     */
    async cleanup() {
        if (this.browser) {
            await this.browser.close();
        }
    }
}

// CLI functionality
async function main() {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log(`
🌐 Website Cloning System

Usage: node website-cloning-system.js <url> [output-directory]

Examples:
  node website-cloning-system.js https://example.com
  node website-cloning-system.js https://github.com my-cloned-github

Features:
  ✅ Complete website cloning
  ✅ Asset downloading (CSS, JS, images)
  ✅ Technology stack detection
  ✅ SEO and accessibility analysis
  ✅ React/Vue component generation
  ✅ Docker configuration
  ✅ Performance metrics
        `);
        return;
    }

    const url = args[0];
    const outputDir = args[1];

    const cloner = new WebsiteCloningSystem();

    try {
        await cloner.initialize();

        const result = await cloner.cloneWebsite(url, {
            outputDir: outputDir
        });

        if (result.success) {
            console.log('\n🎉 Cloning completed successfully!');
            console.log(`📁 Output directory: ${result.outputDir}`);
            console.log(`🌐 Open ${result.outputDir}/index.html in your browser`);
            console.log(`📊 View analysis report: ${result.outputDir}/analysis-report.html`);
            console.log(`⚙️  Integration files: ClonedWebsite.jsx, ClonedWebsite.vue`);
        } else {
            console.error(`❌ Cloning failed: ${result.error}`);
        }

    } finally {
        await cloner.cleanup();
    }
}

// Export for use as module
module.exports = WebsiteCloningSystem;

// Run as CLI if executed directly
if (require.main === module) {
    main().catch(console.error);
}
