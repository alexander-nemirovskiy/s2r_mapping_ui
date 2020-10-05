import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';
import { FileService } from '../services/file.service';
import { LoggerService } from '../services/logger.service';

@Component({
  selector: 'mapping-download',
  templateUrl: './mapping-download.component.html',
  styleUrls: ['./mapping-download.component.scss']
})
export class MappingDownloadComponent implements OnInit {

  constructor(
      private fileService: FileService,
      private logger: LoggerService
  ) { }

  ngOnInit(): void {
  }

  initDownload(){
      const f_id = localStorage.getItem(environment.FILE_ID);
      this.logger.log(`Starting download for: ${f_id}`);
      this.fileService.download_annotated_files(f_id).subscribe(
          data => {
            const blob = new Blob([data], {
                type: 'application/zip'
              });
              const url = window.URL.createObjectURL(blob);
              window.open(url);
          }
      )
  }

}
