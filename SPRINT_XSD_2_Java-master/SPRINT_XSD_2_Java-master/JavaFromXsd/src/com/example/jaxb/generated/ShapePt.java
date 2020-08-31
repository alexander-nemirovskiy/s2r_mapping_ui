package com.example.jaxb.generated;

import java.math.BigDecimal;

public class ShapePt {
	@XmlAttribute(name = "shape_pt_lat", required = true)
	private BigDecimal shapePtLat;
	@XmlAttribute(name = "shape_pt_lon", required = true)
	private BigDecimal shapePtLon;
	@XmlAttribute(name = "shape_dist_traveled")
	private Double shapeDistTraveled;

	public ShapePt() {
	}

	public BigDecimal getShapePtLat() {
		return shapePtLat;
	}

	public void setShapePtLat(BigDecimal shapePtLat) {
		this.shapePtLat = shapePtLat;
	}

	public BigDecimal getShapePtLon() {
		return shapePtLon;
	}

	public void setShapePtLon(BigDecimal shapePtLon) {
		this.shapePtLon = shapePtLon;
	}

	public Double getShapeDistTraveled() {
		return shapeDistTraveled;
	}

	public void setShapeDistTraveled(Double shapeDistTraveled) {
		this.shapeDistTraveled = shapeDistTraveled;
	}
}