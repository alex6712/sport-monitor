import { CommonModule } from '@angular/common';
import {
    Component,
    EventEmitter,
    OnDestroy,
    OnInit,
    Output,
} from '@angular/core';
import {
    ReactiveFormsModule,
    UntypedFormControl,
    UntypedFormGroup,
    Validators,
} from '@angular/forms';
import { TuiAlertService, TuiIcon, TuiLabel } from '@taiga-ui/core';
import { TuiInputModule, TuiInputPasswordModule } from '@taiga-ui/legacy';
import {
    RegisterStatus,
    RegisterStatusOption,
    UserCreate,
} from '../../state/auth/auth.model';
import { AuthService } from '../../state/auth/auth.service';
import { Subscription } from 'rxjs';

@Component({
    selector: 'app-register',
    standalone: true,
    imports: [
        CommonModule,
        TuiInputModule,
        ReactiveFormsModule,
        TuiInputPasswordModule,
        TuiLabel,
        TuiIcon,
    ],
    templateUrl: './register.component.html',
    styleUrl: './register.component.scss',
})
export class RegisterComponent implements OnInit, OnDestroy {
    @Output()
    setFormMode = new EventEmitter<RegisterStatus>();

    private registerDoneSubscription: Subscription | undefined;

    readonly registerFormGroup = new UntypedFormGroup({
        username: new UntypedFormControl('', Validators.required),
        password: new UntypedFormControl('', Validators.required),
        email: new UntypedFormControl('', [
            Validators.required,
            Validators.email,
        ]),
    });

    isLoading = false;
    formMode: RegisterStatusOption = RegisterStatus.Login;

    get isFormInvalid() {
        return this.registerFormGroup.invalid;
    }

    get isFormLogin(): boolean {
        return this.formMode === RegisterStatus.Login;
    }

    constructor(
        private authService: AuthService,
        private alertService: TuiAlertService,
    ) {}

    ngOnInit(): void {
        this.registerDoneSubscription =
            this.authService.registerDone$.subscribe((formMode: string) => {
                if (formMode === RegisterStatus.Login) {
                    this.alertService
                        .open('Регистрация прошла без ошибок.', {
                            label: 'Вы успешно зарегистрированы!',
                            autoClose: 1500,
                            appearance: 'positive',
                        })
                        .subscribe({
                            complete: () => {
                                this.setFormMode.emit(RegisterStatus.Login);
                            },
                        });
                }
            });
    }

    ngOnDestroy(): void {
        this.registerDoneSubscription?.unsubscribe();
    }

    register() {
        const formData = this.registerFormGroup.value;
        this.authService.register(formData as UserCreate);
    }
}
