import { HttpErrorResponse } from "@angular/common/http";

export interface ApiResMessageModel {
    success: boolean;
    status: string;
    message: string;
}

export interface ApiErrorModel extends HttpErrorResponse {
    error: ApiResMessageModel | null;
}