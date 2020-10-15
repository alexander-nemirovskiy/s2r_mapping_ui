import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog'

import { FileService } from '../services/file.service';
import { forkJoin } from 'rxjs';
import { LoggerService } from '../services/logger.service';

@Component({
    selector: 'dialog-upload',
    templateUrl: './dialog-upload.component.html',
    styleUrls: ['./dialog-upload.component.scss']
})
export class DialogUploadComponent implements OnInit {
    @ViewChild('file') file
    public files: Set<File> = new Set()

    constructor(
      public dialogRef: MatDialogRef<DialogUploadComponent>, 
      public uploadService: FileService,
      private logger: LoggerService) { }
    
    ngOnInit(): void { }

    progress;
    canBeClosed = true;
    primaryButtonText = 'Upload';
    showCancelButton = true;
    uploading = false;
    uploadSuccessful = false;

    addFiles() {
        this.file.nativeElement.click();
    }
    
    onFilesAdded(){
        const files: { [key: string]: File } = this.file.nativeElement.files;
        if(this.file.nativeElement.files.length > 5){
            this.logger.warn('More than 5 files selected for upload!');
            alert("You are only allowed to upload a maximum of 5 files at once");
            return false;
        }
        for (let key in files) {
            if (!isNaN(parseInt(key))) {
                this.files.add(files[key]);
            }
        }
    }

    closeDialog() {
        // if everything was uploaded already, just close the dialog
        if (this.uploadSuccessful) {
          return this.dialogRef.close();
        }
      
        // set the component state to "uploading"
        this.uploading = true;
        this.progress = this.uploadService.upload(this.files);
      
        // convert the progress map into an array
        let allProgressObservables = [];
        for (let key in this.progress) {
          allProgressObservables.push(this.progress[key].progress);
        }
      
        // Adjust the state variables
        this.primaryButtonText = 'Finish';
      
        // The dialog should not be closed while uploading
        this.canBeClosed = false;
        this.dialogRef.disableClose = true;
      
        // Hide the cancel-button
        this.showCancelButton = false;
      
        // When all progress-observables are completed...
        forkJoin(allProgressObservables).subscribe(end => {
          // ... the dialog can be closed again...
          this.canBeClosed = true;
          this.dialogRef.disableClose = false;
      
          // ... the upload was successful...
          this.uploadSuccessful = true;
      
          // ... and the component is no longer uploading
          this.uploading = false;
        });
      }
}
