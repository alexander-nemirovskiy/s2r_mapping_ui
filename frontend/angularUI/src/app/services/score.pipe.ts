import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'confidenceScore'})
export class ConfidenceScorePipe implements PipeTransform {
    transform(value: number): string{
        if (value >= 75){
            return 'High confidence';
        }
        else if (value < 75 && value >= 30){
            return 'Medium confidence';
        }
        return 'Low confidence';
    }
}