package com.example.jaxb.generated;

//@RdfProperty(propertyName = "gtfs:trip")
@RdfsClass("gtfs:Trip")
public class Trip {
	@XmlAttribute(name = "route_id", required = true)
	private String routeId;
	@RdfProperty(propertyName = "gtfs:longName")
	//@RdfsClass("gtfs:PickupType")
	@XmlAttribute(name = "service_id", required = true)
	private String serviceId;
	@XmlAttribute(name = "trip_id", required = true)
	private String tripId;
	@XmlAttribute(name = "trip_headsign")
	private String tripHeadsign;
	@XmlAttribute(name = "trip_short_name")
	private String tripShortName;
	@XmlSchemaType(name = "unsignedByte")
	@RdfProperty(propertyName = "gtfs:direction")
	@XmlAttribute(name = "direction_id")
	private Short directionId;
	@RdfProperty(propertyName = "gtfs:block")
	@XmlAttribute(name = "block_id")
	private String blockId;
	@XmlAttribute(name = "shape_id")
	private String shapeId;
	@XmlSchemaType(name = "unsignedByte")
	@RdfProperty(propertyName = "gtfs:bikesAllowed")
	@XmlAttribute(name = "bikes_allowed")
	private Short bikesAllowed;
	@XmlSchemaType(name = "unsignedByte")
	//NotFound
	@RdfProperty(propertyName = "gtfs:wheelchairAccessible")
	//NotFound
	//NotFound
	@XmlAttribute(name = "wheelchair_accessible")
	private Short wheelchairAccessible;

	public Trip() {
	}

	public String getRouteId() {
		return routeId;
	}

	public void setRouteId(String routeId) {
		this.routeId = routeId;
	}

	public String getServiceId() {
		return serviceId;
	}

	public void setServiceId(String serviceId) {
		this.serviceId = serviceId;
	}

	public String getTripId() {
		return tripId;
	}

	public void setTripId(String tripId) {
		this.tripId = tripId;
	}

	public String getTripHeadsign() {
		return tripHeadsign;
	}

	public void setTripHeadsign(String tripHeadsign) {
		this.tripHeadsign = tripHeadsign;
	}

	public String getTripShortName() {
		return tripShortName;
	}

	public void setTripShortName(String tripShortName) {
		this.tripShortName = tripShortName;
	}

	public Short getDirectionId() {
		return directionId;
	}

	public void setDirectionId(Short directionId) {
		this.directionId = directionId;
	}

	public String getBlockId() {
		return blockId;
	}

	public void setBlockId(String blockId) {
		this.blockId = blockId;
	}

	public String getShapeId() {
		return shapeId;
	}

	public void setShapeId(String shapeId) {
		this.shapeId = shapeId;
	}

	public Short getBikesAllowed() {
		return bikesAllowed;
	}

	public void setBikesAllowed(Short bikesAllowed) {
		this.bikesAllowed = bikesAllowed;
	}

	public Short getWheelchairAccessible() {
		return wheelchairAccessible;
	}

	public void setWheelchairAccessible(Short wheelchairAccessible) {
		this.wheelchairAccessible = wheelchairAccessible;
	}
}