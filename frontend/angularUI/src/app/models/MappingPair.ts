export class MappingPair {
    constructor (
        public sourceTerm: string,
        public mappingOptions: string[]
    ) {}
}

export class ChosenFiles {
    constructor (
        public sourceName: string,
        public targetName: string
    ){}
}