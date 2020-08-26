import { Observable, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { LoggerService } from './logger.service';
import { environment } from './../../environments/environment';

const filesURL = environment.API_Endpoint + '/files'

@Injectable({
  providedIn: 'root'
})
export class MappingService {

    constructor(private http: HttpClient, private logger: LoggerService) {}

    getFiles(): Observable<string[]> {
        return this.http.get<string[]>(filesURL)
            .pipe(
                tap(() => this.logger.log('fetched files from server')),
                catchError( err => {
                    this.logger.error('GET failed: ' + err);
                    const message = 'Sorry, GET files failed!';
                    return throwError(message);
                }),
                map((data: string[]) => data)
            );
    }
}
