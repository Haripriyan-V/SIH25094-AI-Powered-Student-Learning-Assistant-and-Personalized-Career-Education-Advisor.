import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import {
  BookOpenIcon,
  BriefcaseIcon,
  ArrowTrendingUpIcon,
  AcademicCapIcon,
} from '@heroicons/react/24/outline';
import api from '../../services/api';
import { Loader } from '../../components/common/Loader';

export default function Dashboard() {
  const [recommendations, setRecommendations] = useState([]);
  const [progress, setProgress] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    Promise.all([
      api.get('/career/my-recommendations/'),
      api.get('/learning/progress/'),
      api.get('/learning/courses/?limit=3'),
    ])
      .then(([recsRes, progRes, coursesRes]) => {
        setRecommendations(Array.isArray(recsRes.data) ? recsRes.data : recsRes.data.results || []);
        const progData = progRes.data;
        setProgress(Array.isArray(progData) ? progData : progData.results || []);
        const coursesData = coursesRes.data;
        setCourses(Array.isArray(coursesData) ? coursesData : coursesData.results || []);
        
        // Get user from localStorage
        const storedUser = localStorage.getItem('disha_user');
        if (storedUser) setUser(JSON.parse(storedUser));
      })
      .catch((err) => console.error('Error loading dashboard:', err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader label="Loading dashboard…" size="lg" />;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-ink-900 dark:text-ink-50 mb-1">
        Welcome, {user?.first_name || user?.username}!
      </h1>
      <p className="text-sm text-ink-500 dark:text-ink-400 mb-8">
        Here's a snapshot of your learning journey and career recommendations.
      </p>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="surface p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase mb-1">Courses</p>
              <p className="text-2xl font-bold text-ink-900 dark:text-ink-50">{progress.length}</p>
            </div>
            <BookOpenIcon className="h-8 w-8 text-iris-500 opacity-20" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="surface p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase mb-1">Progress</p>
              <p className="text-2xl font-bold text-ink-900 dark:text-ink-50">
                {progress.length > 0 ? Math.round(progress.reduce((a, p) => a + p.progress_percent, 0) / progress.length) : 0}%
              </p>
            </div>
            <ArrowTrendingUpIcon className="h-8 w-8 text-growth-500 opacity-20" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="surface p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase mb-1">Career Recommendations</p>
              <p className="text-2xl font-bold text-ink-900 dark:text-ink-50">{recommendations.length}</p>
            </div>
            <BriefcaseIcon className="h-8 w-8 text-marigold-500 opacity-20" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="surface p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase mb-1">Available Courses</p>
              <p className="text-2xl font-bold text-ink-900 dark:text-ink-50">{courses.length}+</p>
            </div>
            <AcademicCapIcon className="h-8 w-8 text-cyan-500 opacity-20" />
          </div>
        </motion.div>
      </div>

      {/* Career Recommendations */}
      {recommendations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-8"
        >
          <h2 className="text-lg font-semibold text-ink-900 dark:text-ink-50 mb-4">Career Recommendations</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {recommendations.slice(0, 2).map((rec) => (
              <div key={rec.id} className="surface p-4">
                <p className="font-semibold text-ink-900 dark:text-ink-50">{rec.career_path_title}</p>
                <p className="text-xs text-iris-500 mb-2">{rec.career_path_career_field_name}</p>
                <p className="text-sm text-ink-500 dark:text-ink-400 mb-3">{rec.reasoning}</p>
                <div className="w-full bg-ink-200 dark:bg-ink-700 rounded-full h-2">
                  <div
                    className="bg-iris-500 h-2 rounded-full transition-all"
                    style={{ width: `${rec.match_score}%` }}
                  />
                </div>
                <p className="text-xs text-ink-400 mt-2 text-right">{rec.match_score}% Match</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Quick Links to Featured Courses */}
      {courses.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <h2 className="text-lg font-semibold text-ink-900 dark:text-ink-50 mb-4">Featured Courses</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {courses.slice(0, 3).map((course) => (
              <div key={course.id} className="surface p-4">
                <p className="font-semibold text-ink-900 dark:text-ink-50 mb-1">{course.title}</p>
                <p className="text-xs text-iris-500 mb-3">{course.subject_name}</p>
                <p className="text-sm text-ink-500 dark:text-ink-400 line-clamp-2 mb-4">{course.description}</p>
                <span className="inline-block px-2 py-1 bg-iris-100 dark:bg-iris-900/40 text-iris-700 dark:text-iris-400 text-xs font-medium rounded capitalize">
                  {course.level}
                </span>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
