import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { DocumentTextIcon, ArrowUpTrayIcon } from '@heroicons/react/24/outline';

export default function Resume() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedResume, setUploadedResume] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) setSelectedFile(file);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setUploading(true);
    // Simulated upload - in real app would send to backend
    setTimeout(() => {
      setUploadedResume(selectedFile.name);
      setSelectedFile(null);
      setUploading(false);
    }, 1000);
  };

  return (
    <div>
      <h1 className="text-2xl font-semibold text-ink-900 dark:text-ink-50 mb-1">Resume Analyzer</h1>
      <p className="text-sm text-ink-500 dark:text-ink-400 mb-6">
        Upload your resume to get ATS score, skill gap analysis, and improvement suggestions.
      </p>

      <div className="max-w-2xl">
        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="surface p-8 mb-6"
        >
          <form onSubmit={handleUpload}>
            <div className="border-2 border-dashed border-ink-300 dark:border-ink-700 rounded-2xl p-8 text-center hover:bg-ink-50 dark:hover:bg-ink-900/50 transition-colors cursor-pointer">
              <input
                type="file"
                onChange={handleFileChange}
                accept=".pdf,.doc,.docx"
                className="hidden"
                id="resume-upload"
              />
              <label htmlFor="resume-upload" className="cursor-pointer">
                <ArrowUpTrayIcon className="h-12 w-12 text-iris-500 mx-auto mb-3" />
                <p className="font-semibold text-ink-900 dark:text-ink-50 mb-1">
                  {selectedFile ? selectedFile.name : 'Upload your resume'}
                </p>
                <p className="text-sm text-ink-500 dark:text-ink-400">
                  PDF, DOC, or DOCX • Max 5MB
                </p>
              </label>
            </div>

            {selectedFile && (
              <button
                type="submit"
                disabled={uploading}
                className="btn-primary w-full mt-4"
              >
                {uploading ? 'Uploading…' : 'Analyze Resume'}
              </button>
            )}
          </form>
        </motion.div>

        {/* Analysis Results (Placeholder) */}
        {uploadedResume && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >
            <div className="surface p-6">
              <h2 className="font-semibold text-ink-900 dark:text-ink-50 mb-4">Resume Analysis</h2>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-medium text-ink-900 dark:text-ink-50">ATS Score</p>
                    <p className="text-2xl font-bold text-iris-600 dark:text-iris-400">78%</p>
                  </div>
                  <div className="w-full bg-ink-200 dark:bg-ink-700 rounded-full h-3">
                    <div className="bg-iris-500 h-3 rounded-full" style={{ width: '78%' }} />
                  </div>
                </div>

                <div>
                  <p className="font-medium text-ink-900 dark:text-ink-50 mb-2">Key Strengths</p>
                  <ul className="space-y-1">
                    <li className="text-sm text-ink-600 dark:text-ink-400">✓ Clear formatting and structure</li>
                    <li className="text-sm text-ink-600 dark:text-ink-400">✓ Relevant keywords present</li>
                    <li className="text-sm text-ink-600 dark:text-ink-400">✓ Professional summary included</li>
                  </ul>
                </div>

                <div>
                  <p className="font-medium text-ink-900 dark:text-ink-50 mb-2">Suggestions for Improvement</p>
                  <ul className="space-y-1">
                    <li className="text-sm text-ink-600 dark:text-ink-400">→ Add more quantified achievements</li>
                    <li className="text-sm text-ink-600 dark:text-ink-400">→ Include industry-specific keywords</li>
                    <li className="text-sm text-ink-600 dark:text-ink-400">→ Reduce resume to 1 page if possible</li>
                  </ul>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Info Card */}
        {!uploadedResume && (
          <div className="bg-iris-50 dark:bg-iris-900/20 border border-iris-200 dark:border-iris-800 rounded-2xl p-6">
            <p className="text-sm text-iris-700 dark:text-iris-300">
              <span className="font-medium">💡 Pro Tip:</span> A good ATS score ensures your resume gets past automated filtering systems. Focus on clear formatting, relevant keywords, and quantifiable achievements.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
