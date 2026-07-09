import { useState } from 'react';
import { motion } from 'framer-motion';
import { CalendarDaysIcon, CheckCircleIcon, PlusIcon } from '@heroicons/react/24/outline';

export default function StudyPlanner() {
  const [todaysGoals, setTodaysGoals] = useState([
    { id: 1, task: 'Complete Python basics module', completed: true },
    { id: 2, task: 'Review algebra concepts', completed: false },
  ]);
  const [newGoal, setNewGoal] = useState('');

  const handleAddGoal = () => {
    if (!newGoal.trim()) return;
    setTodaysGoals([
      ...todaysGoals,
      { id: Date.now(), task: newGoal, completed: false },
    ]);
    setNewGoal('');
  };

  const handleToggleGoal = (id) => {
    setTodaysGoals(
      todaysGoals.map((g) => (g.id === id ? { ...g, completed: !g.completed } : g))
    );
  };

  const completedCount = todaysGoals.filter((g) => g.completed).length;
  const completedPercent = todaysGoals.length > 0 ? Math.round((completedCount / todaysGoals.length) * 100) : 0;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-ink-900 dark:text-ink-50 mb-1">Study Planner</h1>
      <p className="text-sm text-ink-500 dark:text-ink-400 mb-6">
        Plan your study sessions and track daily progress.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Today's Goals */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="lg:col-span-2"
        >
          <div className="surface p-6 mb-6">
            <h2 className="text-lg font-semibold text-ink-900 dark:text-ink-50 mb-4">Today's Goals</h2>

            {/* Progress */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <p className="text-sm font-medium text-ink-600 dark:text-ink-400">
                  {completedCount} of {todaysGoals.length} completed
                </p>
                <p className="text-sm font-bold text-iris-600 dark:text-iris-400">{completedPercent}%</p>
              </div>
              <div className="w-full bg-ink-200 dark:bg-ink-700 rounded-full h-3">
                <div
                  className="bg-iris-500 h-3 rounded-full transition-all"
                  style={{ width: `${completedPercent}%` }}
                />
              </div>
            </div>

            {/* Goals List */}
            <div className="space-y-2 mb-4">
              {todaysGoals.map((goal) => (
                <div
                  key={goal.id}
                  onClick={() => handleToggleGoal(goal.id)}
                  className={`p-3 rounded-xl cursor-pointer transition-colors ${
                    goal.completed
                      ? 'bg-growth-50 dark:bg-growth-900/20'
                      : 'bg-ink-50 dark:bg-ink-900/50 hover:bg-ink-100 dark:hover:bg-ink-900'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`h-5 w-5 rounded-full border-2 flex-shrink-0 flex items-center justify-center ${
                        goal.completed
                          ? 'bg-growth-500 border-growth-500'
                          : 'border-ink-300 dark:border-ink-600'
                      }`}
                    >
                      {goal.completed && <CheckCircleIcon className="h-4 w-4 text-white" />}
                    </div>
                    <p
                      className={`text-sm ${
                        goal.completed
                          ? 'text-growth-700 dark:text-growth-400 line-through'
                          : 'text-ink-900 dark:text-ink-50'
                      }`}
                    >
                      {goal.task}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Add New Goal */}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleAddGoal();
              }}
              className="flex gap-2"
            >
              <input
                type="text"
                value={newGoal}
                onChange={(e) => setNewGoal(e.target.value)}
                placeholder="Add a goal…"
                className="flex-1 input"
              />
              <button type="submit" className="btn-primary">
                <PlusIcon className="h-4 w-4" />
              </button>
            </form>
          </div>
        </motion.div>

        {/* Weekly Schedule */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="surface p-6 h-fit"
        >
          <h2 className="text-lg font-semibold text-ink-900 dark:text-ink-50 mb-4 flex items-center gap-2">
            <CalendarDaysIcon className="h-5 w-5" />
            This Week
          </h2>

          <div className="space-y-3">
            {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].map((day) => (
              <div key={day} className="p-3 rounded-lg bg-ink-50 dark:bg-ink-900/50">
                <p className="text-xs font-medium text-iris-600 dark:text-iris-400 mb-1">{day}</p>
                <p className="text-xs text-ink-500 dark:text-ink-400">2-3 hours planned</p>
              </div>
            ))}
          </div>

          <div className="mt-4 p-3 rounded-lg bg-growth-50 dark:bg-growth-900/20 border border-growth-200 dark:border-growth-800">
            <p className="text-xs font-medium text-growth-700 dark:text-growth-400 mb-1">Total Hours</p>
            <p className="text-xl font-bold text-growth-600 dark:text-growth-400">12 hrs</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
