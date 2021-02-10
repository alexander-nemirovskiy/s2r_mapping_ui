import { Observable, Subject, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { LoggerService } from './logger.service';
import { environment } from './../../environments/environment';
import { MappingPair } from '../models/MappingPair';
import { APIError } from '../models/Errors';

const mappingURL = environment.API_Endpoint + '/mapping';

@Injectable({
  providedIn: 'root'
})
export class MappingService {
    private confirmedPairsSub = new Subject<MappingPair>();
    public confirmedPairs$ = this.confirmedPairsSub.asObservable();

    constructor(private http: HttpClient, private logger: LoggerService) {}

    startMapping(sourceName: string, targetName: string, annotation_type: string): Observable<MappingPair[]> {
        const param = {
            'source_filename': sourceName,
            'target_filename': targetName,
            'annotation_type': annotation_type
        }
        return this.http.get<object>(mappingURL, { params: param })
            .pipe(
                tap(() => this.logger.log('Mapping done')),
                catchError( err => {
                    this.logger.warn('Something wrong happened');
                    if (err.detail && err.status_code){
                        const message = `MAPPING PROCESS failed:\nCODE - [${err.status_code}]\nDETAILS - ${err.detail}`;
                        if (err.detail.code && err.detail.message){
                            return throwError(new APIError(err.status_code, err.detail, err.detail.code, err.detail.message));
                        }
                        return throwError(new APIError(err.status_code, err.detail, null, message));
                    }
                    return throwError(new APIError("500", null, null, "Unexpected server error"));
                }),
                map((data) => {
                    localStorage.setItem('file_id', data['file_id'])
                    let ret: MappingPair[] = []
                    let terms: object = data['terms']
                    let options: object = data['options']
                    let scores: object = data['scores']
                    Object.keys(terms).forEach(key => {
                        const element = new MappingPair(terms[key],options[key],scores[key]);
                        ret.push(element)
                    });
                    return ret;
                })
            );
    }

    confirmMappingPair(pair: MappingPair){
        this.confirmedPairsSub.next(pair);
    }

    finalizeMappings(pairs: MappingPair[]){
        const confirmedPairs: object[] = pairs.map(p => {
            return { [p.sourceTerm]: { 
                [p.mappingOptions[0]]: p.confidenceScores[0] }
            };
        })
        
        this.logger.warn(`Just checking: ${confirmedPairs}`);
        this.logger.dir(confirmedPairs);
        let f_id: string = localStorage.getItem(environment.FILE_ID);
        let body = JSON.stringify({ 
            "file_id":  f_id, 
            "pairs": confirmedPairs
        })
        let options = { 
            headers: new HttpHeaders({
                'Content-Type': 'application/json' 
            }),
        };
        return this.http.post(mappingURL + '/pairs', body)
            .pipe(
                tap(() => this.logger.log('Pairs confirmed')),
                catchError( err => {
                    if (err.detail && err.status_code){
                        const message = `Annotation process failed:\nCODE - [${err.status_code}]\nDETAILS - ${err.detail}`;
                        if (err.detail.code && err.detail.message){
                            return throwError(new APIError(err.status_code, err.detail, err.detail.code, err.detail.message));
                        }
                        return throwError(new APIError(err.status_code, err.detail, null, message));
                    }
                    return throwError(new APIError("500", null, null, "Unexpected server error"));
                })
            );
    }
}
