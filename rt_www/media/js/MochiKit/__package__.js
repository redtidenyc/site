dojo.kwCompoundRequire({
        common: [
        "MochiKit.Base",
        "MochiKit.Iter",
        "MochiKit.Logging",
        "MochiKit.DateTime",
        "MochiKit.Format",
        "MochiKit.Async",
        "MochiKit.Signal",
        "MochiKit.Color"
        ], // a generic dependency
	browser: [
	"MochiKit.DOM",
	"MochiKit.LoggingPane",
	"MochiKit.Visual"
    ]}
);

dojo.provide("MochiKit.*"); 
