import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    full_name: '',
    agree_to_terms: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  
  const { register, error, clearError } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    
    // 清除相关错误
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
    if (error) clearError();
  };

  const validateForm = () => {
    const errors: Record<string, string> = {};
    
    if (!formData.username.trim()) {
      errors.username = '用户名不能为空';
    } else if (formData.username.length < 3) {
      errors.username = '用户名至少需要3个字符';
    }
    
    if (!formData.email.trim()) {
      errors.email = '邮箱不能为空';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = '请输入有效的邮箱地址';
    }
    
    if (!formData.password) {
      errors.password = '密码不能为空';
    } else if (formData.password.length < 8) {
      errors.password = '密码至少需要8个字符';
    }
    
    if (formData.password !== formData.password_confirm) {
      errors.password_confirm = '两次输入的密码不一致';
    }
    
    if (!formData.agree_to_terms) {
      errors.agree_to_terms = '请同意服务条款';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      const success = await register(formData);
      if (success) {
        navigate('/');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            注册 AgentPedia 账户
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            已有账户？{' '}
            <Link
              to="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              立即登录
            </Link>
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <Input
              label="用户名"
              name="username"
              type="text"
              required
              value={formData.username}
              onChange={handleChange}
              placeholder="请输入用户名"
              error={formErrors.username}
            />
            
            <Input
              label="邮箱"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={handleChange}
              placeholder="请输入邮箱地址"
              error={formErrors.email}
            />
            
            <Input
              label="姓名（可选）"
              name="full_name"
              type="text"
              value={formData.full_name}
              onChange={handleChange}
              placeholder="请输入真实姓名"
            />
            
            <Input
              label="密码"
              name="password"
              type="password"
              required
              value={formData.password}
              onChange={handleChange}
              placeholder="请输入密码（至少8位）"
              error={formErrors.password}
            />
            
            <Input
              label="确认密码"
              name="password_confirm"
              type="password"
              required
              value={formData.password_confirm}
              onChange={handleChange}
              placeholder="请再次输入密码"
              error={formErrors.password_confirm}
            />
          </div>

          <div className="flex items-center">
            <input
              id="agree_to_terms"
              name="agree_to_terms"
              type="checkbox"
              checked={formData.agree_to_terms}
              onChange={handleChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label htmlFor="agree_to_terms" className="ml-2 block text-sm text-gray-900">
              我同意{' '}
              <Link to="/terms" className="text-primary-600 hover:text-primary-500">
                服务条款
              </Link>{' '}
              和{' '}
              <Link to="/privacy" className="text-primary-600 hover:text-primary-500">
                隐私政策
              </Link>
            </label>
          </div>
          
          {formErrors.agree_to_terms && (
            <p className="text-sm text-red-600">{formErrors.agree_to_terms}</p>
          )}

          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-700">
                {error}
              </div>
            </div>
          )}

          <Button
            type="submit"
            loading={isLoading}
            disabled={!formData.username || !formData.email || !formData.password || !formData.password_confirm || !formData.agree_to_terms}
            className="w-full"
          >
            注册
          </Button>
        </form>
      </div>
    </div>
  );
};

export default Register;