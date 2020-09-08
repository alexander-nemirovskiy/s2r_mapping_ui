package com.example.jaxb.generated;

//@RdfProperty(propertyName = "gtfs:routeType")
@RdfsClass("gtfs:Route")
//@RdfProperty(propertyName = "gtfs:route")
public class Route {
	@XmlAttribute(name = "route_id", required = true)
	private String routeId;
	@XmlAttribute(name = "agency_id")
	private String agencyId;
	@RdfProperty(propertyName = "gtfs:shortName")
	@XmlAttribute(name = "route_short_name", required = true)
	private String routeShortName;
	@XmlAttribute(name = "route_long_name", required = true)
	private String routeLongName;
	@XmlAttribute(name = "route_desc")
	private String routeDesc;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "route_type", required = true)
	private short routeType;
	@XmlAttribute(name = "route_url")
	private String routeUrl;
	@RdfProperty(propertyName = "gtfs:color")
	@RdfProperty(propertyName = "gtfs:textColor")
	@XmlAttribute(name = "route_color")
	private String routeColor;
	@XmlAttribute(name = "route_text_color")
	private String routeTextColor;

	public Route() {
	}

	public String getRouteId() {
		return routeId;
	}

	public void setRouteId(String routeId) {
		this.routeId = routeId;
	}

	public String getAgencyId() {
		return agencyId;
	}

	public void setAgencyId(String agencyId) {
		this.agencyId = agencyId;
	}

	public String getRouteShortName() {
		return routeShortName;
	}

	public void setRouteShortName(String routeShortName) {
		this.routeShortName = routeShortName;
	}

	public String getRouteLongName() {
		return routeLongName;
	}

	public void setRouteLongName(String routeLongName) {
		this.routeLongName = routeLongName;
	}

	public String getRouteDesc() {
		return routeDesc;
	}

	public void setRouteDesc(String routeDesc) {
		this.routeDesc = routeDesc;
	}

	public short getRouteType() {
		return routeType;
	}

	public void setRouteType(short routeType) {
		this.routeType = routeType;
	}

	public String getRouteUrl() {
		return routeUrl;
	}

	public void setRouteUrl(String routeUrl) {
		this.routeUrl = routeUrl;
	}

	public String getRouteColor() {
		return routeColor;
	}

	public void setRouteColor(String routeColor) {
		this.routeColor = routeColor;
	}

	public String getRouteTextColor() {
		return routeTextColor;
	}

	public void setRouteTextColor(String routeTextColor) {
		this.routeTextColor = routeTextColor;
	}
}