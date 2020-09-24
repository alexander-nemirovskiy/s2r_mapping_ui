import { Component, OnInit, OnDestroy, Output, EventEmitter } from '@angular/core';
import { SubSink } from 'subsink';

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
    @Output() finalizeMapping: EventEmitter<any> = new EventEmitter();

    visible = false;
    localMappings: MappingPair[];
    confirmedItems: MappingPair[] = [];
    
    private subs: SubSink = new SubSink();

    constructor(
        private mappingService: MappingService,
        private notifier: MappingNotifierService, 
        private logger: LoggerService) { }

    ngOnInit(): void {
        this.subs.add(
            this.notifier.notification$.subscribe(
                message => {
                    this.visible = message ? true: false;
                    // this.visible = true;
                    this.logger.log('Notification received');
                    this.localMappings = null;
                    if (message && message.sourceName && message.targetName) {
                        this.subs.add(this.mappingService.startMapping(message.sourceName, message.targetName).subscribe(
                            items => { this.localMappings = items; }
                        ));
                    }
                }
            ),
            this.mappingService.confirmedPairs$.subscribe(
                (pair: MappingPair) => {
                    this.confirmedItems.push(pair);
                }
            )
        );
    }

    finalizeChoice(){
        this.subs.add(this.mappingService.finalizeMappings(this.confirmedItems)
            .subscribe(
                data => {
                    this.finalizeMapping.emit(this);
                    this.logger.log('Confirmation choices received. Ready to delete')
                },
                error => {alert(error)}
            )
        );
    }

    dismissChild($event: MappingPair){
        this.localMappings = this.localMappings.filter(x => x.sourceTerm !== $event.sourceTerm);
    }

    ngOnDestroy(): void {
        this.subs.unsubscribe();
        this.logger.log(`Destroy call made for component ${this}`);
    }

}
