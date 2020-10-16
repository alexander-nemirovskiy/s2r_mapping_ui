import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest, HttpEventType, HttpResponse } from '@angular/common/http'
import { Observable, Subject, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import { LoggerService } from './logger.service';
import { tap, catchError, map } from 'rxjs/operators';
import { APIError } from '../models/Errors';

const uploadURL = environment.API_Endpoint + '/uploads'
const filesURL = environment.API_Endpoint + '/files'

@Injectable({
    providedIn: 'root'
})
export class FileService {
    
    constructor(private http: HttpClient, private logger: LoggerService) {}
    
    getFiles(extensionFilter: string[] = []): Observable<string[]> {
        let param = {}
        if (extensionFilter){
            param = {'extensions': extensionFilter}
        }
        return this.http.get<string[]>(filesURL, { params: param })
            .pipe(
                tap(() => this.logger.log('fetched files from server')),
                catchError( err => {
                    if (err.error) {
                        let error = err.error;
                        if(error.detail && err.status && err.statusText){
                            const message = `File retrieval failed:\nCODE - [${err.statusText}]\nDETAILS - ${error.detail}`;
                            if (error.detail.code && error.detail.message){
                                return throwError(new APIError(error.status, error.detail, error.detail.code, error.detail.message));
                            }
                            return throwError(new APIError(err.status, error.detail, null, message));
                        }
                    }
                    return throwError(new APIError("500", null, null, "Unexpected server error"));
                }),
                map((data: string[]) => data)
            );
    }

    public upload(files: Set<File>):
    { [key: string]: { progress: Observable<number> } } {
        
        const status: { [key: string]: { progress: Observable<number> } } = {};
        
        files.forEach(file => {
            const formData: FormData = new FormData();
            formData.append('file', file, file.name);
            
            const req = new HttpRequest('POST', uploadURL, formData, {
                reportProgress: true
            });
            
            const progress = new Subject<number>();
            
            this.http.request(req).subscribe(event => {
                if (event.type === HttpEventType.UploadProgress) {
                    
                    const percentDone = Math.round(100 * event.loaded / event.total);
                    
                    progress.next(percentDone);
                } else if (event instanceof HttpResponse) {
                    progress.complete();
                }
            });
            
            // Save every progress-observable in a map of all observables
            status[file.name] = {
                progress: progress.asObservable()
            };
        });
        
        // return the map of progress.observables
        return status;
    }

    public download_annotated_files(file_id: string){
        return this.http.get(filesURL + '/' + file_id, {
            responseType: 'arraybuffer'
          });
    }
    
    
}
