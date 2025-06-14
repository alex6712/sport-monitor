import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import {
    ReactiveFormsModule,
    UntypedFormControl,
    UntypedFormGroup,
    Validators,
} from '@angular/forms';
import { TuiInputModule, TuiInputPasswordModule } from '@taiga-ui/legacy';
import { AuthService } from '../../state/auth/auth.service';
import { ActivatedRoute } from '@angular/router';
import {
    RegisterStatus,
    RegisterStatusOption,
    UserLogin,
} from '../../state/auth/auth.model';
import { TuiIcon, TuiLabel, TuiLoader } from '@taiga-ui/core';
import { take } from 'rxjs';
import { CommonModule } from '@angular/common';
import { RegisterComponent } from '../register/register.component';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [
        CommonModule,
        TuiInputModule,
        ReactiveFormsModule,
        TuiInputPasswordModule,
        TuiLoader,
        TuiLabel,
        TuiIcon,
        RegisterComponent,
    ],
    templateUrl: './login.component.html',
    styleUrl: './login.component.scss',
})
export class LoginComponent implements OnInit {
    readonly authFormGroup = new UntypedFormGroup({
        username: new UntypedFormControl('', Validators.required),
        password: new UntypedFormControl('', Validators.required),
    });

    isLoading = false;
    formMode: RegisterStatusOption = RegisterStatus.Login;

    get isFormInvalid() {
        return this.authFormGroup.invalid;
    }

    get isFormLogin(): boolean {
        return this.formMode === RegisterStatus.Login;
    }

    constructor(
        private authService: AuthService,
        private route: ActivatedRoute,
        private cdr: ChangeDetectorRef,
    ) {}

    ngOnInit(): void {
        this.route.queryParams.subscribe((queryParams) => {
            const typeQueryParam = queryParams['type'] as string;
            if (typeQueryParam === RegisterStatus.Register.toLowerCase()) {
                this.formMode = RegisterStatus.Register;
            }
        });
    }

    login(): void {
        this.isLoading = true;
        this.cdr.detectChanges();
        this.authService.login(this.authFormGroup.value as UserLogin);

        this.authService.loginSubject.pipe(take(1)).subscribe(() => {
            this.isLoading = false;
            this.cdr.detectChanges();
        });
    }

    setFormMode(formMode: RegisterStatusOption) {
        this.formMode = formMode;
    }

    setLoginFormMode() {
        this.setFormMode('Login');
    }

    setRegisterFormMode() {
        this.setFormMode('Register');
    }
}
