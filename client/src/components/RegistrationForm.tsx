import React, { useState, useRef } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import axiosInstance from '@/services/api';
import { API_URLS } from '@/services/apiUrls';
import { useSnackbar } from 'notistack';
import { useNavigate } from 'react-router-dom';

const RegisterForm: React.FC = () => {
    const [emailFieldError, setEmailFieldError] = useState<string>("");
    const [passwordFieldError, setPasswordFieldError] = useState<string>("");
    const [confirmPasswordFieldError, setConfirmPasswordFieldError] = useState<string>("");
    const [nameFieldError, setNameFieldError] = useState<string>("");
    const { enqueueSnackbar } = useSnackbar();
    const navigate = useNavigate();
    const emailFieldRef = useRef<HTMLInputElement>(null);
    const passwordFieldRef = useRef<HTMLInputElement>(null);
    const confirmPasswordFieldRef = useRef<HTMLInputElement>(null);
    const nameFieldRef = useRef<HTMLInputElement>(null);

    const validateEmailField = (): boolean => {
        const email = emailFieldRef.current?.value || '';
        if (!email) {
            setEmailFieldError("Error: email cannot be empty.");
            return false;
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            setEmailFieldError("Error: email format is invalid.");
            return false;
        } else {
            setEmailFieldError("");
        }
        return true;
    };

    const validatePasswordField = (): boolean => {
        const password = passwordFieldRef.current?.value || '';
        if (!password) {
            setPasswordFieldError("Error: password cannot be empty.");
            return false;
        } else {
            setPasswordFieldError("");
        }
        return true;
    };

    const validateConfirmPasswordField = (): boolean => {
        const password = passwordFieldRef.current?.value || '';
        const confirmPassword = confirmPasswordFieldRef.current?.value || '';
        if (!confirmPassword) {
            setConfirmPasswordFieldError("Error: confirm password cannot be empty.");
            return false;
        } else if (password !== confirmPassword) {
            setConfirmPasswordFieldError("Error: passwords do not match.");
            return false;
        } else {
            setConfirmPasswordFieldError("");
        }
        return true;
    };

    const validateNameField = (): boolean => {
        const name = nameFieldRef.current?.value || '';
        if (!name) {
            setNameFieldError("Error: name cannot be empty.");
            return false;
        } else {
            setNameFieldError("");
        }
        return true;
    };

    const submitButton = (): void => {
        const isCorrectEmail = validateEmailField();
        const isCorrectPassword = validatePasswordField();
        const isCorrectConfirmPassword = validateConfirmPasswordField();
        const isCorrectName = validateNameField();

        if (!isCorrectEmail || !isCorrectPassword || !isCorrectConfirmPassword || !isCorrectName) {
            return;
        }

        const request = {
            username: nameFieldRef.current?.value,
            email: emailFieldRef.current?.value,
            password: passwordFieldRef.current?.value,
        };

        axiosInstance.post(`${API_URLS.BASE_URL}/register`, request, {
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                console.log(response.data);
                navigate("/create-project")
                enqueueSnackbar('Registration successful.', { variant: 'success' });

            })
            .catch(error => {
                console.error('Error registering:', error);
                enqueueSnackbar('Error registering.', { variant: 'error' });
                return;
            });

    };

    return (
        <div className="isolate px-6 py-24 sm:py-32 lg:px-8">
            <div
                className="absolute inset-x-0 top-[-10rem] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[-20rem]"
                aria-hidden="true"
            >
                <div
                    className="relative left-1/2 -z-10 aspect-[1155/678] w-[36.125rem] max-w-none -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-40rem)] sm:w-[72.1875rem]"
                    style={{
                        clipPath:
                            'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
                    }}
                />
            </div>
            <div className="mx-auto max-w-2xl text-center">
                <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Register</h2>
                <p className="mt-2 text-lg leading-8 text-gray-600">
                    Please enter your name, email and password to register.
                </p>
            </div>
            <div className="mx-auto mt-16 max-w-xl sm:mt-20">
                <div className="grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
                    <div className="sm:col-span-2">
                        <label htmlFor="name" className="block text-sm font-semibold leading-6 ">
                            username
                        </label>
                        <div className="mt-2.5">
                            <Input type="string" ref={nameFieldRef} onChange={() => validateNameField()} />
                            {nameFieldError && <p className='text-xs mt-1 text-red-500'>{nameFieldError}</p>}
                        </div>
                    </div>
                    <div className="sm:col-span-2">
                        <label htmlFor="email" className="block text-sm font-semibold leading-6 ">
                            Email
                        </label>
                        <div className="mt-2.5">
                            <Input type="email" ref={emailFieldRef} onChange={() => validateEmailField()} />
                            {emailFieldError && <p className='text-xs mt-1 text-red-500'>{emailFieldError}</p>}
                        </div>
                    </div>
                    <div className="sm:col-span-2">
                        <label htmlFor="password" className="block text-sm font-semibold leading-6 ">
                            Password
                        </label>
                        <div className="mt-2.5">
                            <Input type="password" ref={passwordFieldRef} onChange={() => validatePasswordField()} />
                            {passwordFieldError && <p className='text-xs mt-1 text-red-500'>{passwordFieldError}</p>}
                        </div>
                    </div>
                    <div className="sm:col-span-2">
                        <label htmlFor="confirm-password" className="block text-sm font-semibold leading-6">
                            Confirm Password
                        </label>
                        <div className="mt-2.5">
                            <Input type="password" ref={confirmPasswordFieldRef} onChange={() => validateConfirmPasswordField()} />
                            {confirmPasswordFieldError && <p className='text-xs mt-1 text-red-500'>{confirmPasswordFieldError}</p>}
                        </div>
                    </div>
                </div>
                <div className="mt-10">
                    <Button
                        onClick={() => submitButton()}
                        type="button"
                        className="block w-full rounded-md bg-indigo-600 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    >
                        Register
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default RegisterForm;
