import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable, Subscription } from 'rxjs';
import { MappingNotifierService } from '../services/mapping-notifier.service';
import { LoggerService } from '../services/logger.service';
import { MappingService } from '../services/mapping.service';
import { MappingPair } from '../models/MappingPair';

@Component({
  selector: 'mapping-container',
  templateUrl: './mapping-container.component.html',
  styleUrls: ['./mapping-container.component.scss']
})
export class MappingContainerComponent implements OnInit, OnDestroy {
    visible = false;
    mappings$: Observable<MappingPair[]>;
    confirmedItems: MappingPair[] = [];
    confirmedItemsSub: Subscription;

    private visibility: Subscription;

    constructor(
        private mappingService: MappingService,
        private notifier: MappingNotifierService, 
        private logger: LoggerService) { }

    ngOnInit(): void {
        this.visibility = this.notifier.notification.subscribe(
            message => {
                this.visible = message;
                this.logger.log('Notification received');
                if (message) {
                    this.mappings$ = this.mappingService.startMapping();
                }
            }
        );
        this.confirmedItemsSub = this.mappingService.confirmedPairs$.subscribe(
            (pair: MappingPair) => {
                this.confirmedItems.push(pair);
            }
        );
    }

    finalizeChoice(){
        this.mappingService.finalizeMappings(this.confirmedItems).subscribe(
            data => {alert(data)},
            error => {alert(error)}
        );
    }

    ngOnDestroy(): void {
        this.visibility.unsubscribe();
        this.confirmedItemsSub.unsubscribe();
    }

}
