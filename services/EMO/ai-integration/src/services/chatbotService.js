const OpenAI = require('openai');
const natural = require('natural');
const compromise = require('compromise');
const logger = require('../utils/logger');

class ChatbotService {
  constructor() {
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY
    });

    this.tokenizer = new natural.WordTokenizer();
    this.classifier = new natural.BayesClassifier();

    // Initialize business-specific training data
    this.initializeClassifier();
  }

  /**
   * Initialize the classifier with business-specific training data
   */
  initializeClassifier() {
    // Business verification queries
    this.classifier.addDocument('How do I verify my business?', 'verification');
    this.classifier.addDocument('What documents do I need?', 'verification');
    this.classifier.addDocument('How long does verification take?', 'verification');
    this.classifier.addDocument('My verification was rejected', 'verification');
    this.classifier.addDocument('Upload business documents', 'verification');

    // SQL level queries
    this.classifier.addDocument('What is SQL level?', 'sql_level');
    this.classifier.addDocument('How to upgrade SQL level?', 'sql_level');
    this.classifier.addDocument('Benefits of higher SQL level', 'sql_level');
    this.classifier.addDocument('SQL level pricing', 'sql_level');

    // Franchise queries
    this.classifier.addDocument('How to become a franchise?', 'franchise');
    this.classifier.addDocument('Franchise requirements', 'franchise');
    this.classifier.addDocument('Franchise benefits', 'franchise');
    this.classifier.addDocument('Franchise territory', 'franchise');

    // Technical support
    this.classifier.addDocument('I cannot login', 'technical');
    this.classifier.addDocument('Website not working', 'technical');
    this.classifier.addDocument('Upload not working', 'technical');
    this.classifier.addDocument('Error message', 'technical');

    // General queries
    this.classifier.addDocument('Hello', 'greeting');
    this.classifier.addDocument('Hi', 'greeting');
    this.classifier.addDocument('Help', 'help');
    this.classifier.addDocument('Contact support', 'contact');

    this.classifier.train();
  }

  /**
   * Process incoming chat message
   */
  async processMessage(messageData) {
    try {
      const { message, userId, context } = messageData;
      
      logger.info(`Processing chat message from user: ${userId}`);

      // Classify the message
      const classification = this.classifyMessage(message);
      
      // Generate response based on classification
      const response = await this.generateResponse(message, classification, context);

      // Log the interaction
      this.logInteraction(userId, message, classification, response);

      return {
        success: true,
        response,
        classification,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      logger.error('Chatbot processing error:', error);
      return {
        success: false,
        response: 'I apologize, but I encountered an error processing your request. Please try again or contact support.',
        error: error.message
      };
    }
  }

  /**
   * Classify the user message
   */
  classifyMessage(message) {
    try {
      const classification = this.classifier.classify(message.toLowerCase());
      const confidence = this.classifier.getClassifications(message.toLowerCase());
      
      return {
        category: classification,
        confidence: confidence.find(c => c.label === classification)?.value || 0,
        allClassifications: confidence
      };
    } catch (error) {
      logger.error('Message classification error:', error);
      return {
        category: 'general',
        confidence: 0,
        allClassifications: []
      };
    }
  }

  /**
   * Generate response based on classification
   */
  async generateResponse(message, classification, context) {
    const { category, confidence } = classification;

    // If confidence is low, use OpenAI for more sophisticated response
    if (confidence < 0.6) {
      return await this.generateOpenAIResponse(message, context);
    }

    // Use predefined responses for high-confidence classifications
    switch (category) {
      case 'verification':
        return this.getVerificationResponse(message);
      
      case 'sql_level':
        return this.getSQLLevelResponse(message);
      
      case 'franchise':
        return this.getFranchiseResponse(message);
      
      case 'technical':
        return this.getTechnicalResponse(message);
      
      case 'greeting':
        return this.getGreetingResponse();
      
      case 'help':
        return this.getHelpResponse();
      
      case 'contact':
        return this.getContactResponse();
      
      default:
        return await this.generateOpenAIResponse(message, context);
    }
  }

  /**
   * Generate response using OpenAI
   */
  async generateOpenAIResponse(message, context) {
    try {
      const systemPrompt = `You are an AI assistant for EMO Business Management System. You help users with:

1. Business verification processes
2. SQL level upgrades and benefits
3. Franchise opportunities
4. Technical support
5. General business management questions

Current context: ${context || 'No specific context'}

Provide helpful, accurate, and concise responses. If you're not sure about something, suggest contacting support.`;

      const completion = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: message }
        ],
        max_tokens: 200,
        temperature: 0.7
      });

      return completion.choices[0].message.content;

    } catch (error) {
      logger.error('OpenAI response generation error:', error);
      return 'I apologize, but I cannot generate a response at the moment. Please try again later or contact support.';
    }
  }

  /**
   * Get verification-related response
   */
  getVerificationResponse(message) {
    const responses = {
      'how do i verify my business': 'To verify your business, please upload the following documents: Business License, Tax Certificate, Bank Statement, and Utility Bill. You can upload these in your dashboard under "Documents" section.',
      'what documents do i need': 'For business verification, you need: 1) Business License, 2) Tax Certificate, 3) Bank Statement, 4) Utility Bill. All documents should be recent (within 3 months).',
      'how long does verification take': 'Business verification typically takes 2-5 business days. We use AI-powered analysis to ensure accuracy and security.',
      'my verification was rejected': 'If your verification was rejected, please check the rejection reason in your dashboard. You can upload additional documents or contact support for assistance.',
      'upload business documents': 'You can upload business documents in your dashboard. Go to "Documents" section and click "Upload Document". Supported formats: PDF, JPG, PNG.'
    };

    const lowerMessage = message.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
      if (lowerMessage.includes(key)) {
        return response;
      }
    }

    return 'For business verification, please upload your business documents in the dashboard. Our AI system will analyze them for authenticity and completeness.';
  }

  /**
   * Get SQL level response
   */
  getSQLLevelResponse(message) {
    const responses = {
      'what is sql level': 'SQL Level determines your access to business features and benefits. Levels: Free (basic), Basic, Normal, High, VIP. Higher levels unlock more features and better support.',
      'how to upgrade sql level': 'To upgrade your SQL level, go to your dashboard and click "Upgrade SQL Level". You can upgrade through our secure payment system.',
      'benefits of higher sql level': 'Higher SQL levels provide: More document uploads, faster verification, priority support, advanced analytics, and exclusive business tools.',
      'sql level pricing': 'SQL Level pricing: Basic ($29/month), Normal ($59/month), High ($99/month), VIP ($199/month). All plans include our AI-powered verification system.'
    };

    const lowerMessage = message.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
      if (lowerMessage.includes(key)) {
        return response;
      }
    }

    return 'SQL Level determines your access to EMO features. You can upgrade in your dashboard to unlock more benefits and faster verification.';
  }

  /**
   * Get franchise response
   */
  getFranchiseResponse(message) {
    const responses = {
      'how to become a franchise': 'To become a franchise, you need: 1) Verified business account, 2) Minimum 6 months business history, 3) Good standing with EMO, 4) Territory availability. Contact our franchise team.',
      'franchise requirements': 'Franchise requirements: Verified business, 6+ months history, good standing, available territory, and commitment to EMO standards.',
      'franchise benefits': 'Franchise benefits: Exclusive territory, commission on sales, marketing support, training, and access to EMO business network.',
      'franchise territory': 'Franchise territories are assigned based on location and market potential. Contact our franchise team to check availability in your area.'
    };

    const lowerMessage = message.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
      if (lowerMessage.includes(key)) {
        return response;
      }
    }

    return 'Franchise opportunities are available for verified businesses. Contact our franchise team to learn more about requirements and benefits.';
  }

  /**
   * Get technical support response
   */
  getTechnicalResponse(message) {
    return 'For technical issues, please try: 1) Clear browser cache, 2) Use a different browser, 3) Check your internet connection. If the problem persists, contact our technical support team at support@emo.com';
  }

  /**
   * Get greeting response
   */
  getGreetingResponse() {
    const greetings = [
      'Hello! How can I help you with your EMO business account today?',
      'Hi there! Welcome to EMO Business Management. How can I assist you?',
      'Greetings! I\'m here to help with your business verification and management needs.',
      'Welcome! How can I support your EMO business journey today?'
    ];
    
    return greetings[Math.floor(Math.random() * greetings.length)];
  }

  /**
   * Get help response
   */
  getHelpResponse() {
    return 'I can help you with: Business verification, SQL level upgrades, franchise opportunities, technical support, and general questions. What would you like to know?';
  }

  /**
   * Get contact response
   */
  getContactResponse() {
    return 'You can contact us at: Email: support@emo.com, Phone: +1-800-EMO-HELP, or through the contact form in your dashboard. Our support team is available 24/7.';
  }

  /**
   * Extract entities from message
   */
  extractEntities(message) {
    try {
      const doc = compromise(message);
      
      return {
        organizations: doc.organizations().out('array'),
        places: doc.places().out('array'),
        dates: doc.dates().out('array'),
        numbers: doc.numbers().out('array'),
        emails: doc.emails().out('array')
      };
    } catch (error) {
      logger.error('Entity extraction error:', error);
      return {};
    }
  }

  /**
   * Log chat interaction
   */
  logInteraction(userId, message, classification, response) {
    try {
      logger.info(`Chat interaction - User: ${userId}, Message: "${message}", Classification: ${classification.category}, Confidence: ${classification.confidence}`);
      
      // Here you could save to database for analytics
      // await ChatLog.create({ userId, message, classification, response, timestamp: new Date() });
      
    } catch (error) {
      logger.error('Chat interaction logging error:', error);
    }
  }

  /**
   * Get chat analytics
   */
  async getChatAnalytics(userId = null, dateRange = null) {
    try {
      // This would typically query the database for chat logs
      // For now, return basic analytics
      return {
        totalInteractions: 0,
        averageResponseTime: 0,
        topCategories: [],
        userSatisfaction: 0
      };
    } catch (error) {
      logger.error('Chat analytics error:', error);
      throw new Error('Failed to get chat analytics');
    }
  }

  /**
   * Update chatbot training data
   */
  async updateTrainingData(newData) {
    try {
      // Add new training examples
      newData.forEach(item => {
        this.classifier.addDocument(item.input, item.category);
      });
      
      // Retrain the classifier
      this.classifier.train();
      
      logger.info('Chatbot training data updated successfully');
      
    } catch (error) {
      logger.error('Training data update error:', error);
      throw new Error('Failed to update training data');
    }
  }
}

module.exports = new ChatbotService(); 