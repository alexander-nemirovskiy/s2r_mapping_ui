import { NgModule } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';

@NgModule({
    imports: [
        MatTableModule,
        MatProgressSpinnerModule,
        MatButtonModule,
        MatIconModule,
        MatDialogModule,
        MatInputModule,
        MatFormFieldModule,
        MatToolbarModule,
        MatSidenavModule,
        MatListModule,
        MatTabsModule,
        MatCardModule,
    ],
    exports: [
        MatTableModule,
        MatProgressSpinnerModule,
        MatButtonModule,
        MatIconModule,
        MatDialogModule,
        MatInputModule,
        MatFormFieldModule,
        MatToolbarModule,
        MatSidenavModule,
        MatListModule,
        MatTabsModule,
        MatCardModule,
    ]
})
export class MaterialModule { }
