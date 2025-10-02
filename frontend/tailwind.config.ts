import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // 主色调
        primary: {
          DEFAULT: '#FFFFFF',
          dark: '#111111',
        },
        // 次级背景
        secondary: {
          DEFAULT: '#F5F7FA',
          dark: '#1E1E1E',
        },
        // 强调色（黑色系）
        accent: {
          DEFAULT: '#000000',
          dark: '#000000',
          hover: 'rgba(0, 0, 0, 0.1)',
          glow: 'rgba(0, 0, 0, 0.2)',
        },
        // 表面颜色
        surface: {
          DEFAULT: '#FFFFFF',
          dark: '#111111',
        },
        // 背景颜色
        background: {
          DEFAULT: '#FFFFFF',
          dark: '#111111',
        },
        // 文本颜色
        text: {
          primary: {
            DEFAULT: '#1D2129',
            dark: '#E5E7EB',
          },
          secondary: {
            DEFAULT: '#4E5969',
            dark: '#8A8F98',
          },
        },
        // 边框
        border: {
          DEFAULT: '#E5E6EB',
          dark: '#2D2D2D',
        },
        // 状态色
        success: '#36CFC9',
        warning: '#FFA940',
        error: '#FF4D4F',
        info: '#000000',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(0, 0, 0, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(0, 0, 0, 0.8)' },
        },
      },
      boxShadow: {
        'glow': '0 0 20px rgba(0, 0, 0, 0.8)',
        'glow-sm': '0 0 10px rgba(0, 0, 0, 0.6)',
        'card': '0 2px 8px rgba(0, 0, 0, 0.05)',
        'card-dark': '0 2px 8px rgba(0, 0, 0, 0.3)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}

export default config