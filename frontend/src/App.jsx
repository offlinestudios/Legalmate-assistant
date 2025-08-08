import React, { useState, useRef, useEffect } from 'react'
import { Button } from './components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card'
import { Input } from './components/ui/input'
import { Textarea } from './components/ui/textarea'
import { 
  Send, 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX, 
  FileText, 
  Shield, 
  MessageSquare, 
  Scale, 
  AlertTriangle, 
  FileCheck,
  Languages,
  Menu,
  PanelLeft,
  Settings,
  HelpCircle,
  User,
  Crown,
  LogOut,
  Upload,
  X,
  ChevronDown
} from 'lucide-react'
import './App.css'

function App() {
  const [documentText, setDocumentText] = useState('')
  const [analysisResult, setAnalysisResult] = useState('')
  const [selectedMode, setSelectedMode] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [showHelpModal, setShowHelpModal] = useState(false)
  const [showSettingsModal, setShowSettingsModal] = useState(false)
  const [showPricingModal, setShowPricingModal] = useState(false)
  const [showReleaseNotesModal, setShowReleaseNotesModal] = useState(false)
  const [showHelpMenu, setShowHelpMenu] = useState(false)
  const [showAccountMenu, setShowAccountMenu] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [uploadedFile, setUploadedFile] = useState(null)e)
  const [analysis, setAnalysis] = useState('')
  
  // Chatbot states
  const [chatMessages, setChatMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      message: "Hi! I'm LegalMate, your AI legal assistant. I'm here to help you understand contracts, identify risks, negotiate better terms, and answer your legal questions. How can I assist you today?",
      timestamp: new Date()
    }
  ])
  const [chatInput, setChatInput] = useState('')
  const [isChatMode, setIsChatMode] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [voiceEnabled, setVoiceEnabled] = useState(true)
  
  const chatEndRef = useRef(null)
  const recognitionRef = useRef(null)
  const synthRef = useRef(null)

  const aiModes = [
    {
      id: 'translator',
      title: 'Translator Mode',
      description: 'Explain this contract in plain English',
      icon: Brain,
      color: 'bg-blue-500',
      emoji: '🧑‍🎓'
    },
    {
      id: 'risk',
      title: 'Risk Mode',
      description: "What's sketchy or one-sided in this document?",
      icon: Shield,
      color: 'bg-red-500',
      emoji: '🕵️'
    },
    {
      id: 'negotiator',
      title: 'Negotiator Mode',
      description: 'Propose a fairer version of this clause',
      icon: MessageSquare,
      color: 'bg-green-500',
      emoji: '✍️'
    },
    {
      id: 'agent',
      title: 'Agent Mode',
      description: 'What terms should I ask for in this deal?',
      icon: Handshake,
      color: 'bg-purple-500',
      emoji: '💼'
    },
    {
      id: 'dispute',
      title: 'Dispute Mode',
      description: 'Help me get my money back',
      icon: AlertTriangle,
      color: 'bg-orange-500',
      emoji: '📢'
    },
    {
      id: 'template',
      title: 'Template Mode',
      description: 'Generate legal documents and forms',
      icon: FileText,
      color: 'bg-indigo-500',
      emoji: '📃'
    }
  ]

  const suggestedPrompts = [
    "Review this freelance contract for red flags",
    "What should I negotiate in my lease agreement?",
    "Help me write a professional complaint letter",
    "Generate a simple NDA template",
    "Explain this clause in plain English",
    "What are my rights as a tenant?",
    "How do I terminate this contract safely?",
    "What payment terms should I ask for?"
  ]

  // Initialize speech recognition and synthesis
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = false
      recognitionRef.current.lang = 'en-US'

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript
        setChatInput(transcript)
        setIsListening(false)
      }

      recognitionRef.current.onerror = () => {
        setIsListening(false)
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    }

    if ('speechSynthesis' in window) {
      synthRef.current = window.speechSynthesis
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
      if (synthRef.current) {
        synthRef.current.cancel()
      }
    }
  }, [])

  // Auto-scroll chat to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true)
      recognitionRef.current.start()
    }
  }

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    }
  }

  const speakText = (text) => {
    if (synthRef.current && voiceEnabled) {
      synthRef.current.cancel()
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.9
      utterance.pitch = 1
      utterance.volume = 0.8
      
      utterance.onstart = () => setIsSpeaking(true)
      utterance.onend = () => setIsSpeaking(false)
      utterance.onerror = () => setIsSpeaking(false)
      
      synthRef.current.speak(utterance)
    }
  }

  const stopSpeaking = () => {
    if (synthRef.current) {
      synthRef.current.cancel()
      setIsSpeaking(false)
    }
  }

  const handleChatSubmit = async (message = chatInput) => {
    if (!message.trim()) return

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      message: message.trim(),
      timestamp: new Date()
    }

    setChatMessages(prev => [...prev, userMessage])
    setChatInput('')

    // Show typing indicator
    const typingMessage = {
      id: Date.now() + 1,
      sender: 'bot',
      message: 'typing...',
      timestamp: new Date(),
      isTyping: true
    }
    setChatMessages(prev => [...prev, typingMessage])

    try {
      const response = await fetch('https://5000-ioppahmjq6bl5js6b4gmn-fb8d72ff.manusvm.computer/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message.trim(),
          context: chatMessages.slice(-5) // Send last 5 messages for context
        })
      })

      const data = await response.json()
      
      // Remove typing indicator
      setChatMessages(prev => prev.filter(msg => !msg.isTyping))

      if (data.success) {
        const botMessage = {
          id: Date.now() + 2,
          sender: 'bot',
          message: data.response,
          timestamp: new Date()
        }
        setChatMessages(prev => [...prev, botMessage])
        
        // Speak the response if voice is enabled
        if (voiceEnabled) {
          speakText(data.response)
        }
      } else {
        const errorMessage = {
          id: Date.now() + 2,
          sender: 'bot',
          message: "I apologize, but I'm having trouble processing your request right now. Please try again or use the document analysis feature above.",
          timestamp: new Date()
        }
        setChatMessages(prev => [...prev, errorMessage])
      }
    } catch (error) {
      // Remove typing indicator
      setChatMessages(prev => prev.filter(msg => !msg.isTyping))
      
      const errorMessage = {
        id: Date.now() + 2,
        sender: 'bot',
        message: "I'm currently having connection issues. Please try again in a moment or use the document analysis feature above.",
        timestamp: new Date()
      }
      setChatMessages(prev => [...prev, errorMessage])
    }
  }

  const handleDocumentAnalysis = async () => {
    if (!documentText.trim() || !selectedMode) return
    
    setIsAnalyzing(true)
    try {
      const response = await fetch('https://5000-ioppahmjq6bl5js6b4gmn-fb8d72ff.manusvm.computer/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document: documentText,
          mode: selectedMode
        })
      })

      const data = await response.json()
      
      if (data.success) {
        setAnalysis(data.analysis)
        
        // Also add to chat if in chat mode
        if (isChatMode) {
          const analysisMessage = {
            id: Date.now(),
            sender: 'bot',
            message: `**Document Analysis (${selectedMode.charAt(0).toUpperCase() + selectedMode.slice(1)} Mode):**\n\n${data.analysis}`,
            timestamp: new Date()
          }
          setChatMessages(prev => [...prev, analysisMessage])
        }
      } else {
        setAnalysis('Error: ' + (data.error || 'Unable to analyze document'))
      }
    } catch (error) {
      setAnalysis('Error: Unable to connect to analysis service')
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                LegalMate
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="secondary" className="bg-pink-100 text-pink-700">Free Trial</Badge>
              <Button variant="outline" size="sm">Sign In</Button>
              <Button size="sm" className="bg-gradient-to-r from-blue-600 to-purple-600">Get Started</Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Mode Toggle */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg p-1 shadow-sm border">
            <Button
              variant={!isChatMode ? "default" : "ghost"}
              onClick={() => setIsChatMode(false)}
              className="rounded-md"
            >
              <FileText className="w-4 h-4 mr-2" />
              Document Analysis
            </Button>
            <Button
              variant={isChatMode ? "default" : "ghost"}
              onClick={() => setIsChatMode(true)}
              className="rounded-md"
            >
              <Bot className="w-4 h-4 mr-2" />
              Chat with LegalMate
            </Button>
          </div>
        </div>

        {!isChatMode ? (
          /* Document Analysis Mode */
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="text-center space-y-4">
              <h2 className="text-4xl font-bold text-gray-900">Your AI Legal Helper</h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                24/7 AI-powered legal assistant for contracts, negotiations, and disputes. No $300/hour lawyer fees. 
                Get instant legal guidance for freelancers, tenants, creators, and small business owners.
              </p>
              <div className="flex justify-center space-x-4 text-sm text-gray-500">
                <span className="flex items-center"><Shield className="w-4 h-4 mr-1" />Contract Review</span>
                <span className="flex items-center"><AlertTriangle className="w-4 h-4 mr-1" />Risk Detection</span>
                <span className="flex items-center"><MessageSquare className="w-4 h-4 mr-1" />Negotiation Help</span>
                <span className="flex items-center"><FileText className="w-4 h-4 mr-1" />Legal Templates</span>
              </div>
            </div>

            {/* AI Modes */}
            <div>
              <h3 className="text-2xl font-bold text-center mb-6">Choose Your AI Legal Assistant Mode</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {aiModes.map((mode) => (
                  <Card 
                    key={mode.id}
                    className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                      selectedMode === mode.id ? 'ring-2 ring-blue-500 shadow-lg' : ''
                    }`}
                    onClick={() => setSelectedMode(mode.id)}
                  >
                    <CardHeader className="pb-3">
                      <div className="flex items-center space-x-3">
                        <div className={`w-10 h-10 ${mode.color} rounded-lg flex items-center justify-center text-white text-lg`}>
                          {mode.emoji}
                        </div>
                        <div>
                          <CardTitle className="text-lg">{mode.title}</CardTitle>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-sm">{mode.description}</CardDescription>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Document Upload */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Upload className="w-5 h-5" />
                  <span>Upload or Paste Your Document</span>
                </CardTitle>
                <CardDescription>
                  Paste your contract, lease, or legal document below for AI analysis
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="Paste your legal document text here..."
                  value={documentText}
                  onChange={(e) => setDocumentText(e.target.value)}
                  className="min-h-[200px] resize-none"
                />
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-500">
                    {selectedMode ? `Selected: ${aiModes.find(m => m.id === selectedMode)?.title}` : 'Please select an AI mode above'}
                  </span>
                  <Button 
                    onClick={handleDocumentAnalysis}
                    disabled={!documentText.trim() || !selectedMode || isAnalyzing}
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                  >
                    {isAnalyzing ? 'Analyzing...' : 'Analyze Document'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Analysis Results */}
            {analysis && (
              <Card>
                <CardHeader>
                  <CardTitle>AI Analysis Result</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="prose max-w-none">
                    <p className="whitespace-pre-wrap">{analysis}</p>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Pricing */}
            <div className="text-center space-y-8">
              <h3 className="text-3xl font-bold">Simple, Transparent Pricing</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
                <Card>
                  <CardHeader>
                    <CardTitle>Free</CardTitle>
                    <CardDescription>Get started with basic features</CardDescription>
                    <div className="text-3xl font-bold">$0</div>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <p className="text-sm">• 3 document uploads/month</p>
                    <p className="text-sm">• Basic contract summaries</p>
                    <p className="text-sm">• Limited AI modes</p>
                    <Button className="w-full mt-4" variant="outline">Get Started</Button>
                  </CardContent>
                </Card>

                <Card className="border-blue-200 relative">
                  <Badge className="absolute -top-2 left-1/2 transform -translate-x-1/2 bg-blue-600">Most Popular</Badge>
                  <CardHeader>
                    <CardTitle>Pro</CardTitle>
                    <CardDescription>For regular legal needs</CardDescription>
                    <div className="text-3xl font-bold">$12.99<span className="text-sm font-normal">/month</span></div>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <p className="text-sm">• Unlimited document reviews</p>
                    <p className="text-sm">• All AI modes</p>
                    <p className="text-sm">• Negotiation tools</p>
                    <p className="text-sm">• Letter generation</p>
                    <Button className="w-full mt-4 bg-gradient-to-r from-purple-600 to-blue-600">Start Pro Trial</Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Agent+</CardTitle>
                    <CardDescription>Advanced legal strategy</CardDescription>
                    <div className="text-3xl font-bold">$29.99<span className="text-sm font-normal">/month</span></div>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <p className="text-sm">• Everything in Pro</p>
                    <p className="text-sm">• Legal strategy prompts</p>
                    <p className="text-sm">• Deal agent mode</p>
                    <p className="text-sm">• Access to paralegals</p>
                    <Button className="w-full mt-4" variant="outline">Contact Sales</Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        ) : (
          /* Chat Mode */
          <div className="max-w-4xl mx-auto">
            <Card className="h-[600px] flex flex-col">
              <CardHeader className="border-b">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                      <Bot className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <CardTitle>Chat with LegalMate</CardTitle>
                      <CardDescription>Your AI legal assistant is ready to help</CardDescription>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setVoiceEnabled(!voiceEnabled)}
                      className={voiceEnabled ? "text-blue-600" : "text-gray-400"}
                    >
                      {voiceEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
                    </Button>
                    {isSpeaking && (
                      <Button variant="ghost" size="sm" onClick={stopSpeaking}>
                        <VolumeX className="w-4 h-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </CardHeader>

              {/* Chat Messages */}
              <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
                {chatMessages.map((msg) => (
                  <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`flex items-start space-x-2 max-w-[80%] ${msg.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        msg.sender === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                      }`}>
                        {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                      </div>
                      <div className={`rounded-lg p-3 ${
                        msg.sender === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gray-100 text-gray-900'
                      }`}>
                        {msg.isTyping ? (
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                          </div>
                        ) : (
                          <p className="text-sm whitespace-pre-wrap">{msg.message}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={chatEndRef} />
              </CardContent>

              {/* Suggested Prompts */}
              {chatMessages.length <= 1 && (
                <div className="px-4 pb-2">
                  <p className="text-sm text-gray-600 mb-2">Try asking:</p>
                  <div className="flex flex-wrap gap-2">
                    {suggestedPrompts.slice(0, 4).map((prompt, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        size="sm"
                        onClick={() => handleChatSubmit(prompt)}
                        className="text-xs"
                      >
                        {prompt}
                      </Button>
                    ))}
                  </div>
                </div>
              )}

              {/* Chat Input */}
              <div className="border-t p-4">
                <div className="flex items-center space-x-2">
                  <div className="flex-1 relative">
                    <Input
                      placeholder="Ask me anything about contracts, legal rights, or get help with documents..."
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleChatSubmit()}
                      className="pr-12"
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      className={`absolute right-1 top-1/2 transform -translate-y-1/2 ${
                        isListening ? 'text-red-500' : 'text-gray-400'
                      }`}
                      onClick={isListening ? stopListening : startListening}
                    >
                      {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                    </Button>
                  </div>
                  <Button 
                    onClick={() => handleChatSubmit()}
                    disabled={!chatInput.trim()}
                    className="bg-gradient-to-r from-blue-600 to-purple-600"
                  >
                    <Send className="w-4 h-4" />
                  </Button>
                </div>
                {isListening && (
                  <p className="text-xs text-blue-600 mt-1 flex items-center">
                    <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse mr-2"></div>
                    Listening... Speak now
                  </p>
                )}
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

