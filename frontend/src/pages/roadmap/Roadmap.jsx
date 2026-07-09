import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircleIcon, ClockIcon } from '@heroicons/react/24/outline';
import api from '../../services/api';
import { Loader } from '../../components/common/Loader';

export default function Roadmap() {
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .get('/learning/progress/')
      .then((res) => {
        const data = res.data;
        setProgress(Array.isArray(data) ? data : data.results || []);
      })
      .catch((err) => {
        console.error('Error fetching progress:', err);
        setError('Failed to load learning roadmap.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader label="Loading roadmap…" size="lg" />;

  const completed = progress.filter((p) => p.status === 'completed').length;
  const inProgress = progress.filter((p) => p.status === 'in_progress').length;
  const notStarted = progress.filter((p) => p.status === 'not_started').length;
  const totalProgress = progress.length > 0 ? Math.round((completed / progress.length) * 100) : 0;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-ink-900 dark:text-ink-50 mb-1">Learning Roadmap</h1>
      <p className="text-sm text-ink-500 dark:text-ink-400 mb-6">
        Track your learning journey through courses and milestones.
      </p>

      {error && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 dark:bg-rose-900/20 dark:border-rose-800 p-4 text-sm text-rose-600 dark:text-rose-400 mb-6">
          {error}
        </div>
      )}

      {/* Summary Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-8">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="surface p-4">
          <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase mb-1">Total Progress</p>
          <p className="text-2xl font-bold text-iris-600 dark:text-iris-400">{totalProgress}%</p>
          <div className="w-full bg-ink-200 dark:bg-ink-700 rounded-full h-2 mt-2">
            <div className="bg-iris-500 h-2 rounded-full" style={{ width: `${totalProgress}%` }} />
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="surface p-4">
          <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase mb-1">Completed</p>
          <p className="text-2xl font-bold text-growth-600 dark:text-growth-400">{completed}</p>
          <p className="text-xs text-ink-400 dark:text-ink-500 mt-1">Courses finished</p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="surface p-4">
          <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase mb-1">In Progress</p>
          <p className="text-2xl font-bold text-marigold-600 dark:text-marigold-400">{inProgress}</p>
          <p className="text-xs text-ink-400 dark:text-ink-500 mt-1">Currently learning</p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="surface p-4">
          <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase mb-1">Not Started</p>
          <p className="text-2xl font-bold text-ink-400 dark:text-ink-600">{notStarted}</p>
          <p className="text-xs text-ink-400 dark:text-ink-500 mt-1">Available courses</p>
        </motion.div>
      </div>

      {/* Timeline */}
      {progress.length === 0 ? (
        <div className="text-center py-12">
          <ClockIcon className="h-12 w-12 text-ink-300 dark:text-ink-600 mx-auto mb-3" />
          <p className="text-ink-500 dark:text-ink-400">No courses started yet.</p>
          <a href="/courses" className="btn-primary inline-block mt-4">Browse Courses</a>
        </div>
      ) : (
        <div className="space-y-4">
          {progress.map((p, idx) => (
            <motion.div
              key={p.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.05 }}
              className="surface p-5 flex items-center justify-between gap-4"
            >
              <div className="flex items-start gap-4 flex-1">
                {p.status === 'completed' ? (
                  <CheckCircleIcon className="h-6 w-6 text-growth-500 shrink-0 mt-1" />
                ) : (
                  <div className={`h-6 w-6 rounded-full border-2 shrink-0 mt-1 ${
                    p.status === 'in_progress'
                      ? 'border-iris-500 bg-iris-50 dark:bg-iris-900/20'
                      : 'border-ink-300 dark:border-ink-700'
                  }`} />
                )}
                <div className="flex-1">
                  <p className={`font-semibold ${
                    p.status === 'completed'
                      ? 'text-growth-700 dark:text-growth-400 line-through'
                      : 'text-ink-900 dark:text-ink-50'
                  }`}>
                    {p.course_title}
                  </p>
                  <p className="text-xs text-ink-500 dark:text-ink-400 capitalize">
                    {p.status.replace('_', ' ')}
                  </p>
                </div>
              </div>

              {/* Progress bar */}
              <div className="w-32 flex-shrink-0">
                <div className="w-full bg-ink-200 dark:bg-ink-700 rounded-full h-2">
                  <div
                    className="bg-iris-500 h-2 rounded-full transition-all"
                    style={{ width: `${p.progress_percent}%` }}
                  />
                </div>
                <p className="text-xs text-ink-400 dark:text-ink-500 text-right mt-1">
                  {p.progress_percent}%
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
