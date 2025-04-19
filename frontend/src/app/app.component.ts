import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { SharedComponent } from './shared/shared/shared.component';
import { ModulesComponent } from './modules/modules.component';
import { TuiRoot } from '@taiga-ui/core';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [
        RouterOutlet,
        CommonModule,
        FormsModule,
        SharedComponent,
        ModulesComponent,
        TuiRoot,
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppComponent {
    title = 'frontend';
}
