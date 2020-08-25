import { UploadService } from './services/upload.service';
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
import {  HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ToolbarComponent,
    Base404Component,
    FileUploadComponent,
    DialogUploadComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule
  ],
  providers: [UploadService, HttpClientModule],
  bootstrap: [AppComponent]
})
export class AppModule { }
