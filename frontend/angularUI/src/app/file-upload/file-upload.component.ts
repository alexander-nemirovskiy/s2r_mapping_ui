import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog'
import { FileService } from '../services/file.service';
import { DialogUploadComponent } from '../dialog-upload/dialog-upload.component';

@Component({
  selector: 'file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: [ './file-upload.component.scss'  ]
})
export class FileUploadComponent{
    constructor(public dialog: MatDialog, public uploadService: FileService) {}

    public openUploadDialog() {
      let dialogRef = this.dialog.open(DialogUploadComponent, {
        width: '50%',
        height: '50%',
      })
    }
}
