import React, { useState, useRef, useEffect } from 'react';

// Types
type Message = {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  subAgent?: string;
  thoughts?: string[];
};

// Mock product data for the storefront
const PRODUCTS = [
  { id: 1, name: 'Minimalist Chair', price: '$129.00', image: 'https://images.unsplash.com/photo-1592078615290-033ee584e267?w=500&q=80', tag: 'Bestseller' },
  { id: 2, name: 'Ceramic Table Lamp', price: '$89.00', image: 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=500&q=80', tag: 'New Arrival' },
  { id: 3, name: 'Linen Throw Blanket', price: '$55.00', image: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=500&q=80' },
  { id: 4, name: 'Oak Wood Desk', price: '$399.00', image: 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=500&q=80' },
];

export default function App() {
  // Chat state
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "👋 Welcome to ShopSmart! I'm your AI shopping assistant. Feel free to ask me for product recommendations or check on an existing order.",
      sender: 'agent',
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());

  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = chatContainerRef.current;
    if (container) {
      // If user is within 100px of bottom, scroll to bottom
      const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100;
      if (isNearBottom) {
        container.scrollTo({
          top: container.scrollHeight,
          behavior: 'smooth'
        });
      }
    }
  }, [messages]);

  // Handle chat submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.text,
          customer_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch response');
      }

      const data = await response.json();

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: 'agent',
        subAgent: data.sub_agent_used,
        thoughts: data.thoughts,
      };

      setMessages((prev) => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, our AI services are temporarily offline. Please try again later.",
        sender: 'agent',
        subAgent: 'system',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fafafa] font-sans text-gray-900 selection:bg-amber-100 selection:text-amber-900 flex flex-col relative">

      {/* Announcement Bar */}
      <div className="bg-gray-900 text-white text-xs sm:text-sm font-medium tracking-wide py-2 text-center uppercase">
        Free shipping on all orders over $50 | Shop the Spring Sale
      </div>

      {/* Main Navigation (Shopify Style) */}
      <nav className="bg-white border-b border-gray-100 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Mobile Menu Icon */}
            <div className="flex md:hidden items-center">
              <button className="text-gray-600 hover:text-gray-900">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
              </button>
            </div>

            {/* Left Nav (Desktop) */}
            <div className="hidden md:flex space-x-8 items-center flex-1">
              <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors uppercase tracking-widest">Shop</a>
              <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors uppercase tracking-widest">About</a>
              <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors uppercase tracking-widest">Journal</a>
            </div>

            {/* Logo */}
            <div className="flex items-center justify-center flex-1">
              <span className="font-serif text-3xl md:text-4xl tracking-tighter text-gray-900 italic font-bold">
                ShopSmart
              </span>
            </div>

            {/* Right Nav Icons */}
            <div className="flex items-center justify-end space-x-5 flex-1">
              <button className="text-gray-600 hover:text-gray-900 hidden sm:block">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              </button>
              <button className="text-gray-600 hover:text-gray-900 hidden sm:block">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
              </button>
              <button className="text-gray-600 hover:text-gray-900 relative">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
                <span className="absolute -top-1.5 -right-2 bg-gray-900 text-white text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">0</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Banner */}
      <div className="relative w-full h-[50vh] min-h-[400px] mb-12">
        <img
          src="https://images.unsplash.com/photo-1616486029423-aaa4789e8c9a?w=1600&q=80"
          alt="Interior Design Hero"
          className="w-full h-full object-cover grayscale opacity-80"
        />
        <div className="absolute inset-0 bg-gray-900/40 mix-blend-multiply"></div>
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-6">
          <h1 className="text-white text-5xl md:text-7xl font-serif font-medium mb-6 drop-shadow-lg tracking-tight">Meet Your AI Assistant</h1>
          <p className="text-white text-lg md:text-xl mb-8 font-light drop-shadow-md max-w-2xl px-4">
            Discover products, track orders, and get expert design advice instantly through our embedded AI concierge.
          </p>
        </div>
      </div>

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24 w-full">

        {/* Chat Interface Embedded in Page */}
        <div className="mb-24 -mt-32 relative z-10 bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden flex flex-col lg:flex-row">

          {/* Left Side: Information */}
          <div className="lg:w-1/3 p-10 bg-gray-900 text-white flex flex-col">
            <div className="flex-1">
              <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center mb-6">
                <svg className="w-6 h-6 text-amber-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
              </div>
              <h2 className="text-2xl font-serif font-bold mb-4">ShopSmart AI Support</h2>
              <p className="text-gray-300 text-sm leading-relaxed mb-8">
                Experience the future of e-commerce. Our specialized AI agents can help you discover new products, track your shipments, or process returns instantly.
              </p>

              <div className="space-y-3">
                <div className="bg-white/5 border border-white/10 p-4 rounded-xl cursor-default">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-amber-300 mb-1">Try asking</p>
                  <p className="text-sm font-medium text-white">"Can you recommend a laptop?"</p>
                </div>
                <div className="bg-white/5 border border-white/10 p-4 rounded-xl cursor-default">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-blue-300 mb-1">Try tracking</p>
                  <p className="text-sm font-medium text-white">"Where is order #10001?"</p>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-white/10 flex items-center gap-3 opacity-60">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
              <span className="text-xs uppercase tracking-widest font-bold">Systems Operational</span>
            </div>
          </div>

          {/* Right Side: Chat App */}
          <div className="lg:w-2/3 flex flex-col h-[600px] bg-[#fafafa]">
            {/* Chat Messages */}
            <div
              ref={chatContainerRef}
              className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6"
            >
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'
                    }`}
                >
                  {msg.subAgent && msg.sender === 'agent' && (
                    <div className="flex items-center gap-1 mb-1.5 ml-1 opacity-80">
                      <span className="text-[9px] font-bold text-indigo-600 uppercase tracking-widest border border-indigo-100 px-2 py-0.5 rounded bg-indigo-50">
                        {msg.subAgent.replace('_', ' ')}
                      </span>
                    </div>
                  )}

                  <div
                    className={`max-w-[90%] px-5 py-3.5 rounded-2xl text-[15px] leading-relaxed relative ${msg.sender === 'user'
                      ? 'bg-gray-900 text-white rounded-br-sm shadow-md'
                      : 'bg-white text-gray-800 rounded-bl-sm border border-gray-200 shadow-sm'
                      }`}
                    style={{ whiteSpace: 'pre-wrap' }}
                  >
                    {msg.text}

                    {msg.thoughts && msg.thoughts.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-100">
                        <details className="group">
                          <summary className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-indigo-500 cursor-pointer list-none hover:text-indigo-700 transition-colors">
                            <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></span>
                            View Thought Process
                            <svg className="w-3 h-3 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                          </summary>
                          <div className="mt-2 space-y-2">
                            {msg.thoughts.map((thought, i) => (
                              <div key={i} className="flex gap-2">
                                <span className="text-gray-400 font-serif italic text-xs">💭</span>
                                <p className="text-xs text-gray-500 font-medium italic leading-relaxed">{thought}</p>
                              </div>
                            ))}
                          </div>
                        </details>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex flex-col items-start">
                  <div className="bg-white border border-gray-200 px-6 py-5 rounded-2xl rounded-bl-sm shadow-sm flex items-center space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              )}
              <div />
            </div>

            {/* Chat Input */}
            <div className="p-4 md:p-6 bg-white border-t border-gray-100">
              <form onSubmit={handleSubmit} className="flex gap-3 relative">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask me anything..."
                  className="w-full bg-gray-50 border border-gray-200 text-gray-900 text-base rounded-xl px-5 py-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all pr-16"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="absolute right-2 top-2 bottom-2 px-5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shrink-0 shadow-sm"
                >
                  <svg className="w-5 h-5 font-bold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                </button>
              </form>
              <div className="text-center mt-3">
                <span className="text-[10px] text-gray-400 font-medium uppercase tracking-widest">Powered by ShopSmart Multi-Agent architecture</span>
              </div>
            </div>
          </div>
        </div>

        {/* Product Grid */}
        <div className="mb-10 text-center">
          <h2 className="text-2xl md:text-3xl font-serif font-medium text-gray-900">Featured Collection</h2>
          <div className="w-16 h-0.5 bg-gray-900 mx-auto mt-4"></div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-y-10 gap-x-6 xl:gap-x-8">
          {PRODUCTS.map((product) => (
            <div key={product.id} className="group relative flex flex-col cursor-pointer">
              <div className="relative w-full aspect-[4/5] bg-gray-100 overflow-hidden mb-4">
                <img
                  src={product.image}
                  alt={product.name}
                  className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-700 ease-out"
                />
                {product.tag && (
                  <div className="absolute top-3 left-3 bg-white/90 backdrop-blur-sm px-2.5 py-1 text-[10px] uppercase tracking-widest font-bold text-gray-900">
                    {product.tag}
                  </div>
                )}
                {/* Quick Add overlay */}
                <div className="absolute bottom-0 left-0 right-0 p-4 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
                  <button className="w-full bg-white text-gray-900 text-sm font-medium py-3 opacity-95 hover:opacity-100 shadow-sm transition-opacity">
                    Quick Add
                  </button>
                </div>
              </div>
              <h3 className="text-sm font-medium text-gray-900 truncate">
                {product.name}
              </h3>
              <p className="mt-1 text-sm text-gray-500">{product.price}</p>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white pt-16 pb-8 border-t border-gray-100 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          <div>
            <span className="font-serif text-2xl tracking-tighter italic font-bold mb-6 block">ShopSmart</span>
            <p className="text-sm text-gray-400 leading-relaxed">
              Curating high-quality, sustainable goods for the modern home.
            </p>
          </div>
          <div>
            <h4 className="text-sm uppercase tracking-widest font-bold mb-6">Shop</h4>
            <ul className="space-y-4 text-sm text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">All Products</a></li>
              <li><a href="#" className="hover:text-white transition-colors">New Arrivals</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Furniture</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Lighting</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm uppercase tracking-widest font-bold mb-6">Support</h4>
            <ul className="space-y-4 text-sm text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Shipping & Returns</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Contact Us</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm uppercase tracking-widest font-bold mb-6">Newsletter</h4>
            <p className="text-sm text-gray-400 mb-4">Subscribe to receive updates, access to exclusive deals, and more.</p>
            <div className="flex border-b border-gray-700 pb-2 focus-within:border-white transition-colors">
              <input type="email" placeholder="Enter your email address" className="bg-transparent border-none outline-none text-sm w-full text-white placeholder-gray-500" />
              <button className="text-sm uppercase tracking-widest font-bold ml-2">Subscribe</button>
            </div>
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-gray-500 pt-8 border-t border-gray-800">
          © 2026 ShopSmart Demo. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
