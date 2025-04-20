// The exported code uses Tailwind CSS. Install Tailwind CSS in your dev environment to ensure all styles work.

import React, { useState, useEffect } from 'react';

const App: React.FC = () => {
  const [showModal, setShowModal] = useState<boolean>(false);
  const [title, setTitle] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [pains, setPains] = useState<Array<{id: number, title: string, description: string, votes: number}>>([
    { id: 1, title: 'Slow API Response Times', description: 'Our third-party payment API is taking 3-5 seconds to respond, causing user dropoff during checkout.', votes: 42 },
    { id: 2, title: 'User Onboarding Confusion', description: 'New users are getting lost during the onboarding process and abandoning signup.', votes: 37 },
    { id: 3, title: 'Mobile Responsiveness Issues', description: 'Our dashboard breaks on smaller screens, making it unusable for mobile users.', votes: 29 },
    { id: 4, title: 'Integration Complexity', description: 'Connecting our system with legacy databases requires too much custom code.', votes: 23 },
    { id: 5, title: 'Search Performance', description: 'Search results take too long to load when the database grows beyond 10,000 records.', votes: 18 },
    { id: 6, title: 'User Permission Management', description: 'Managing role-based access control is becoming increasingly complex as we add more features.', votes: 15 },
  ]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title.trim() && description.trim()) {
      const newPain = {
        id: pains.length > 0 ? Math.max(...pains.map(p => p.id)) + 1 : 1,
        title,
        description,
        votes: 0
      };
      setPains([newPain, ...pains]);
      setTitle('');
      setDescription('');
      setShowModal(false);
    }
  };

  const handleVote = (id: number) => {
    setPains(pains.map(pain => 
      pain.id === id ? { ...pain, votes: pain.votes + 1 } : pain
    ));
  };

  return (
    <div className="min-h-screen bg-[#FAFAFA] font-sans">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-[#1C2B3A]">Pain Library</h1>
            <p className="text-gray-500 text-sm">Real problems. Real projects.</p>
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="bg-[#F5F5DC] text-[#1C2B3A] px-6 py-2 rounded-lg font-medium hover:shadow-md transition-all duration-200 transform hover:scale-105 whitespace-nowrap cursor-pointer !rounded-button"
          >
            <i className="fas fa-plus-circle mr-2"></i>
            Share Your Pain
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto pt-24 pb-16 px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {pains.map(pain => (
            <div 
              key={pain.id}
              className="bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200 transform hover:translate-y-[-4px] overflow-hidden"
            >
              <div className="p-6">
                <h3 className="text-lg font-semibold text-[#1C2B3A] mb-2">{pain.title}</h3>
                <p className="text-gray-700 mb-6">{pain.description}</p>
                <div className="flex items-center justify-between">
                  <button 
                    onClick={() => handleVote(pain.id)}
                    className="flex items-center text-[#1C2B3A] hover:text-[#FFE4E1] transition-colors cursor-pointer !rounded-button whitespace-nowrap"
                  >
                    <i className="fas fa-fire text-[#F5F5DC] hover:text-[#FFE4E1] text-xl mr-2 transition-all duration-200"></i>
                    <span>I feel this pain</span>
                  </button>
                  <div className="bg-[#F5F5DC] px-3 py-1 rounded-full text-[#1C2B3A] font-medium">
                    {pain.votes} <span className="text-sm">votes</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-lg max-w-md w-full p-6 animate-fade-in">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-[#1C2B3A]">Share Your Pain</h2>
              <button 
                onClick={() => setShowModal(false)}
                className="text-gray-500 hover:text-gray-700 cursor-pointer !rounded-button whitespace-nowrap"
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label htmlFor="title" className="block text-gray-700 mb-2">Title</label>
                <input
                  type="text"
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1C2B3A] focus:border-transparent"
                  placeholder="What's the pain point?"
                  required
                />
              </div>
              <div className="mb-6">
                <label htmlFor="description" className="block text-gray-700 mb-2">Description</label>
                <textarea
                  id="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1C2B3A] focus:border-transparent h-32 resize-none"
                  placeholder="Describe the problem in detail..."
                  required
                ></textarea>
              </div>
              <div className="flex justify-end gap-3">
                <button 
                  type="button" 
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors cursor-pointer !rounded-button whitespace-nowrap"
                >
                  Cancel
                </button>
                <button 
                  type="submit"
                  className="bg-[#1C2B3A] text-white px-6 py-2 rounded-lg hover:bg-opacity-90 transition-colors cursor-pointer !rounded-button whitespace-nowrap"
                >
                  Submit
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
};

export default App;

