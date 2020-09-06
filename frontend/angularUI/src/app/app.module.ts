import { FileService } from './services/file.service';
import { MaterialModule } from './material.module';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HomeComponent } from './home/home.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { Base404Component } from './base404/base404.component';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { DialogUploadComponent } from './dialog-upload/dialog-upload.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MappingSelectorComponent } from './mapping-selector/mapping-selector.component';
import { FileManagerComponent } from './file-manager/file-manager.component';
import { FileSelectComponent } from './file-select/file-select.component';
import { MappingContainerComponent } from './mapping-container/mapping-container.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ToolbarComponent,
    Base404Component,
    FileUploadComponent,
    DialogUploadComponent,
    MappingSelectorComponent,
    MappingContainerComponent,
    FileManagerComponent,
    FileSelectComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [FileService, HttpClientModule],
  bootstrap: [AppComponent]
})
export class AppModule { }
