import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable, Subscription } from 'rxjs';
import { MappingNotifierService } from '../services/mapping-notifier.service';
import { LoggerService } from '../services/logger.service';

@Component({
  selector: 'mapping-container',
  templateUrl: './mapping-container.component.html',
  styleUrls: ['./mapping-container.component.scss']
})
export class MappingContainerComponent implements OnInit, OnDestroy {
    visible = false;
    mappings$: Observable<object[]>;

    private visibility: Subscription;

    constructor(private notifier: MappingNotifierService, private logger: LoggerService) { }

    ngOnInit(): void {
        this.visibility = this.notifier.notification.subscribe(
            message => {
                this.visible = message;
                this.logger.log('Notification received');
            }
        );
    }

    ngOnDestroy(): void {
        this.visibility.unsubscribe();
    }

}
