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

    startMapping(sourceName: string, targetName: string): Observable<MappingPair[]> {
        const param = {
            'source_filename': sourceName,
            'target_filename': targetName
        }
        return this.http.get<object>(mappingURL, { params: param })
            .pipe(
                tap(() => this.logger.log('Mapping done')),
                catchError( err => {
                    this.logger.error('MAPPING PROCESS failed: ' + err);
                    this.logger.dir(err)
                    const message = 'Sorry, GET mapping failed!';
                    return throwError(message);
                }),
                map((data) => {
                    localStorage.setItem('file_id', data['file_id'])
                    let dataPairs: object = data['pairs']
                    let ret: MappingPair[] = []
                    Object.keys(dataPairs).forEach(key => {
                        const element = new MappingPair(key,dataPairs[key]);
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
        let file_id = localStorage.getItem('file_id');
        return this.http.post(mappingURL + '/pairs', { confirmedPairs: confirmedPairs, file_id: file_id })
            .pipe(
                tap(() => this.logger.log('Pairs confirmed')),
                catchError( err => {
                    this.logger.error('Finalize mappings failed: ' + err);
                    this.logger.dir(err);
                    const message = 'Sorry, POST pair confirmation failed!';
                    return throwError(message);
                })
            );
    }
}
