export interface UserLogin {
    username: string;
    password: string;
}

export interface UserCreate extends UserLogin {
    email: string;
}

export interface UserData {
    id: string;
    username: string;
}

export interface AuthState extends UserData {
    access_token: string;
    refresh_token: string;
    token_type: string;
    loading: boolean;
}

export interface RefreshTokenData {
    id: string;
    name: string;
    token: string;
}

export enum RegisterStatus {
    Login = 'Login',
    Register = 'Register',
}

export type RegisterStatusOption = keyof typeof RegisterStatus;
