import { Observable, Subject, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { LoggerService } from './logger.service';
import { environment } from './../../environments/environment';
import { MappingPair } from '../models/MappingPair';

const mappingURL = environment.API_Endpoint + '/mapping';

@Injectable({
  providedIn: 'root'
})
export class MappingService {
    private confirmedPairsSub = new Subject<MappingPair>();
    public confirmedPairs$ = this.confirmedPairsSub.asObservable();

    constructor(private http: HttpClient, private logger: LoggerService) {}

    startMapping(): Observable<MappingPair[]> {
        let param = {
            'source_filename': 'gtfs.ttl',
            'target_filename': 'gtfs.ttl'
        }
        return this.http.get<object[]>(mappingURL, { params: param })
            .pipe(
                tap(() => this.logger.log('Mapping done')),
                catchError( err => {
                    this.logger.error('GET failed: ' + err);
                    const message = 'Sorry, GET mapping failed!';
                    return throwError(message);
                }),
                map((data) => {
                    let ret: MappingPair[] = []
                    Object.keys(data).forEach(key => {
                        const element = new MappingPair(key,data[key]);
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
        const confirmedPairs = pairs.map(p => {
            return { [p.sourceTerm]: p.mappingOptions[0] };
        })
        this.logger.warn(`Just checking: ${confirmedPairs}`);
            
        return this.http.post(mappingURL + '/pairs', confirmedPairs)
            .pipe(
                tap(() => this.logger.log('Pairs confirmed')),
                catchError( err => {
                    this.logger.error('POST failed: ' + err);
                    const message = 'Sorry, POST pair confirmation failed!';
                    return throwError(message);
                })
            );
    }
}
