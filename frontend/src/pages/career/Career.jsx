import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BriefcaseIcon, ArrowTrendingUpIcon, SparklesIcon } from '@heroicons/react/24/outline';
import api from '../../services/api';
import { Loader } from '../../components/common/Loader';

export default function Career() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .get('/career/my-recommendations/')
      .then((res) => {
        setRecommendations(Array.isArray(res.data) ? res.data : res.data.results || []);
      })
      .catch((err) => {
        console.error('Error fetching recommendations:', err);
        setError('Failed to load recommendations. Please try again.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader label="Loading recommendations…" size="lg" />;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-ink-900 dark:text-ink-50 mb-1">Career Guidance</h1>
      <p className="text-sm text-ink-500 dark:text-ink-400 mb-6">
        Personalized career recommendations based on your skills and interests.
      </p>

      {error && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 dark:bg-rose-900/20 dark:border-rose-800 p-4 text-sm text-rose-600 dark:text-rose-400 mb-6">
          {error}
        </div>
      )}

      {recommendations.length === 0 ? (
        <div className="text-center py-12">
          <SparklesIcon className="h-12 w-12 text-ink-300 dark:text-ink-600 mx-auto mb-3" />
          <p className="text-ink-500 dark:text-ink-400 mb-4">
            No recommendations yet. Complete a skill assessment to get started!
          </p>
          <a href="/assessment" className="btn-primary inline-block">
            Take Assessment
          </a>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {recommendations.map((rec, idx) => (
            <motion.div
              key={rec.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="surface p-6"
            >
              {/* Header */}
              <div className="flex items-start justify-between gap-4 mb-4">
                <div className="flex-1">
                  <h2 className="text-lg font-semibold text-ink-900 dark:text-ink-50 mb-1">
                    {rec.career_path_title}
                  </h2>
                  <p className="text-sm text-iris-500 font-medium">
                    {rec.career_path_career_field_name}
                  </p>
                </div>
                <BriefcaseIcon className="h-6 w-6 text-iris-500 opacity-20 shrink-0" />
              </div>

              {/* Match Score */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase">Match Score</p>
                  <p className="text-sm font-bold text-iris-600 dark:text-iris-400">{rec.match_score}%</p>
                </div>
                <div className="w-full bg-ink-200 dark:bg-ink-700 rounded-full h-3">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${rec.match_score}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                    className="bg-gradient-iris h-3 rounded-full"
                  />
                </div>
              </div>

              {/* Details */}
              {rec.career_path_average_salary_lpa && (
                <div className="mb-3 flex items-center gap-2">
                  <ArrowTrendingUpIcon className="h-4 w-4 text-marigold-500" />
                  <span className="text-sm text-ink-600 dark:text-ink-400">
                    Avg. ₹{Number(rec.career_path_average_salary_lpa).toLocaleString('en-IN')} LPA
                  </span>
                </div>
              )}

              {rec.career_path_growth_outlook && (
                <div className="mb-4 flex items-center gap-2">
                  <SparklesIcon className="h-4 w-4 text-growth-500" />
                  <span className="text-sm text-ink-600 dark:text-ink-400 capitalize">
                    Growth: {rec.career_path_growth_outlook.replace('_', ' ')}
                  </span>
                </div>
              )}

              {/* Reasoning */}
              <div className="p-3 rounded-lg bg-iris-50 dark:bg-iris-900/20 border border-iris-100 dark:border-iris-800">
                <p className="text-xs font-medium text-iris-700 dark:text-iris-400 mb-1">Why This Fit?</p>
                <p className="text-sm text-iris-600 dark:text-iris-300 line-clamp-3">
                  {rec.reasoning || 'Based on your skills and interests.'}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}