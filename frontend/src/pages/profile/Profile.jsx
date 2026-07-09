import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import {
  UserIcon,
  EnvelopeIcon,
  PhoneIcon,
  BookOpenIcon,
  SparklesIcon,
  AcademicCapIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import api from '../../services/api';
import { Loader } from '../../components/common/Loader';

function EditableField({ label, value, onChange, type = 'text' }) {
  const [isEditing, setIsEditing] = useState(false);
  const [fieldValue, setFieldValue] = useState(value);

  const handleSave = () => {
    onChange(fieldValue);
    setIsEditing(false);
  };

  return (
    <div className="mb-4">
      <label className="text-xs font-medium text-ink-500 dark:text-ink-400 uppercase tracking-wide">
        {label}
      </label>
      {isEditing ? (
        <div className="mt-1 flex gap-2">
          <input
            type={type}
            value={fieldValue}
            onChange={(e) => setFieldValue(e.target.value)}
            className="flex-1 rounded-xl border border-ink-200 dark:border-ink-700 bg-white dark:bg-ink-900 px-3 py-2 text-sm"
          />
          <button
            onClick={handleSave}
            className="btn-primary"
          >
            Save
          </button>
          <button
            onClick={() => {
              setFieldValue(value);
              setIsEditing(false);
            }}
            className="btn-ghost"
          >
            Cancel
          </button>
        </div>
      ) : (
        <div
          onClick={() => setIsEditing(true)}
          className="mt-1 rounded-xl bg-ink-50 dark:bg-ink-900 px-3 py-2 text-sm cursor-pointer hover:bg-ink-100 dark:hover:bg-ink-800 transition-colors"
        >
          {value || '–'}
        </div>
      )}
    </div>
  );
}

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [education, setEducation] = useState([]);
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    Promise.all([
      api.get('/students/profile/me/'),
      api.get('/students/education/'),
      api.get('/students/my-skills/'),
    ])
      .then(([profileRes, educationRes, skillsRes]) => {
        setProfile(profileRes.data);
        const eduData = educationRes.data;
        setEducation(Array.isArray(eduData) ? eduData : eduData.results || []);
        const skillsData = skillsRes.data;
        setSkills(Array.isArray(skillsData) ? skillsData : skillsData.results || []);
      })
      .catch((err) => {
        console.error('Error fetching profile:', err);
        setError('Failed to load profile. Please try again.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader label="Loading profile…" size="lg" />;

  if (error) return <div className="text-sm text-rose-600 dark:text-rose-400">{error}</div>;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-ink-900 dark:text-ink-50 mb-6">Student Profile</h1>

      {/* Tabs */}
      <div className="mb-6 flex gap-2 border-b border-ink-200 dark:border-ink-800">
        {['profile', 'education', 'skills'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 font-medium text-sm transition-colors ${
              activeTab === tab
                ? 'text-iris-600 dark:text-iris-400 border-b-2 border-iris-500'
                : 'text-ink-500 dark:text-ink-400 hover:text-ink-700 dark:hover:text-ink-300'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Profile Tab */}
      {activeTab === 'profile' && profile && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="surface max-w-2xl p-6"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="h-16 w-16 rounded-full bg-gradient-to-br from-iris-500 to-violet-600 flex items-center justify-center text-white text-xl font-bold">
              {profile.user_username?.[0]?.toUpperCase()}
            </div>
            <div>
              <h2 className="text-lg font-semibold text-ink-900 dark:text-ink-50">
                {profile.user_first_name} {profile.user_last_name}
              </h2>
              <p className="text-sm text-iris-500">@{profile.user_username}</p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <EnvelopeIcon className="h-4 w-4 text-ink-400" />
              <span className="text-sm text-ink-500">{profile.user_email}</span>
            </div>

            <EditableField
              label="First Name"
              value={profile.user_first_name || ''}
              onChange={(val) => setProfile({ ...profile, user_first_name: val })}
            />
            <EditableField
              label="Last Name"
              value={profile.user_last_name || ''}
              onChange={(val) => setProfile({ ...profile, user_last_name: val })}
            />
            <EditableField
              label="Phone"
              value={profile.phone_number || ''}
              onChange={(val) => setProfile({ ...profile, phone_number: val })}
              type="tel"
            />
            <EditableField
              label="Bio"
              value={profile.bio || ''}
              onChange={(val) => setProfile({ ...profile, bio: val })}
            />
            <EditableField
              label="School/College"
              value={profile.school_or_college || ''}
              onChange={(val) => setProfile({ ...profile, school_or_college: val })}
            />
            <EditableField
              label="Grade/Class"
              value={profile.grade_or_class || ''}
              onChange={(val) => setProfile({ ...profile, grade_or_class: val })}
            />
          </div>
        </motion.div>
      )}

      {/* Education Tab */}
      {activeTab === 'education' && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          {education.length === 0 ? (
            <div className="text-center py-12">
              <BookOpenIcon className="h-12 w-12 text-ink-300 dark:text-ink-600 mx-auto mb-3" />
              <p className="text-ink-500 dark:text-ink-400">No education records yet.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {education.map((edu) => (
                <div key={edu.id} className="surface p-4">
                  <h3 className="font-semibold text-ink-900 dark:text-ink-50">{edu.institution_name}</h3>
                  <p className="text-sm text-iris-500">{edu.degree_or_level}</p>
                  {edu.field_of_study && <p className="text-xs text-ink-500">{edu.field_of_study}</p>}
                  <p className="text-xs text-ink-400 mt-2">
                    {edu.start_year} – {edu.end_year || 'Present'}
                  </p>
                  {edu.percentage_or_gpa && <p className="text-xs text-ink-400">GPA: {edu.percentage_or_gpa}</p>}
                </div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      {/* Skills Tab */}
      {activeTab === 'skills' && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          {skills.length === 0 ? (
            <div className="text-center py-12">
              <SparklesIcon className="h-12 w-12 text-ink-300 dark:text-ink-600 mx-auto mb-3" />
              <p className="text-ink-500 dark:text-ink-400">No skills added yet.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {skills.map((skill) => (
                <div key={skill.id} className="surface p-4 flex items-center justify-between">
                  <div>
                    <p className="font-medium text-ink-900 dark:text-ink-50">{skill.skill_name}</p>
                    <p className="text-xs text-ink-500 capitalize">{skill.proficiency}</p>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium capitalize ${
                      skill.proficiency === 'advanced'
                        ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400'
                        : skill.proficiency === 'intermediate'
                        ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400'
                        : 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-400'
                    }`}
                  >
                    {skill.proficiency}
                  </span>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
}
