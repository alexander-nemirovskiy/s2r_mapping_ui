import { Observable, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { LoggerService } from './logger.service';
import { environment } from './../../environments/environment';

const mappingURL = environment.API_Endpoint + '/mapping';

@Injectable({
  providedIn: 'root'
})
export class MappingService {

    constructor(private http: HttpClient, private logger: LoggerService) {}

    startMapping(): Observable<JSON> {
        return this.http.get<JSON>(mappingURL)
            .pipe(
                tap(() => this.logger.log('fetched files from server')),
                catchError( err => {
                    this.logger.error('GET failed: ' + err);
                    const message = 'Sorry, GET files failed!';
                    return throwError(message);
                }),
                // map((data: string[]) => data)
            );
    }
}
