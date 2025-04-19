export interface UserBase {
    username: string;
    email: string;
}

export interface User extends UserBase {
    id: string;
}
