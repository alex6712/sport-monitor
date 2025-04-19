import { HttpErrorResponse } from '@angular/common/http';

export interface ApiResMessageModel {
    code: number;
    message: string;
}

export interface ApiErrorModel extends HttpErrorResponse {
    error: ApiResMessageModel | null;
}
