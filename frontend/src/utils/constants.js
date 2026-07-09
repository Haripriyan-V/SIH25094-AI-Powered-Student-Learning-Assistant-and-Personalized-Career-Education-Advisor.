export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

export const ROLES = {
  STUDENT: 'student',
  COUNSELOR: 'counselor',
  ADMIN: 'admin',
};

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
  CHAT: '/chat',
  CAREER: '/career',
  ROADMAP: '/roadmap',
  ASSESSMENT: '/assessment',
  COURSES: '/courses',
  SCHOLARSHIPS: '/scholarships',
  COLLEGES: '/colleges',
  RESOURCES: '/resources',
  EXAMS: '/exams',
  RESUME: '/resume',
  PLANNER: '/planner',
  NOTIFICATIONS: '/notifications',
  SETTINGS: '/settings',
  ABOUT: '/about',
  CONTACT: '/contact',
};
