package com.example.jaxb.generated;

@RdfsClass("gtfs:ServiceRule")
public class FareRule {
	@XmlSchemaType(name = "unsignedByte")
	//@RdfsClass("gtfs:FareClass")
	@RdfProperty(propertyName = "gtfs:fareUrl")
	//@RdfsClass("gtfs:FareRule")
	@XmlAttribute(name = "fare_id", required = true)
	private short fareId;
	@XmlAttribute(name = "route_id")
	private String routeId;
	@RdfProperty(propertyName = "gtfs:originZone")
	@XmlAttribute(name = "origin_id")
	private String originId;
	@RdfProperty(propertyName = "gtfs:destinationZone")
	@XmlAttribute(name = "destination_id")
	private String destinationId;
	@XmlAttribute(name = "contains_id")
	private String containsId;

	public FareRule() {
	}

	public short getFareId() {
		return fareId;
	}

	public void setFareId(short fareId) {
		this.fareId = fareId;
	}

	public String getRouteId() {
		return routeId;
	}

	public void setRouteId(String routeId) {
		this.routeId = routeId;
	}

	public String getOriginId() {
		return originId;
	}

	public void setOriginId(String originId) {
		this.originId = originId;
	}

	public String getDestinationId() {
		return destinationId;
	}

	public void setDestinationId(String destinationId) {
		this.destinationId = destinationId;
	}

	public String getContainsId() {
		return containsId;
	}

	public void setContainsId(String containsId) {
		this.containsId = containsId;
	}
}