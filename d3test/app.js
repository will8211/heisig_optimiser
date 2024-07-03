// app.js

const width = 1200;
const height = 800;

const svg = d3
  .select("body")
  .append("svg")
  .attr("width", width)
  .attr("height", height);

// Define the Nodes and Links

const nodes = [
  {
    id: "G",
    label: "占\ntell fortunes (44)",
    background: "./assets/Medium.png",
  },
  {
    id: "E",
    label: "卜\ndivination (43)",
  },
  {
    id: "C",
    label: "丨\nwalking stick (primitive)",
  },
  { id: "B", label: "一\none (1)", background: "./assets/Elementary.png" },
  {
    id: "D",
    label: "丶\na drop of (primitive)",
  },
  {
    id: "F",
    label: "口\nmouth (11)",
    background: "./assets/Elementary.png",
  },
];

const links = [
  { source: "E", target: "G", thickness: 2 },
  { source: "C", target: "E", thickness: 2 },
  { source: "B", target: "C", thickness: 2 },
  { source: "D", target: "E", thickness: 2 },
  { source: "F", target: "G", thickness: 2 },
];

// Create and Style Nodes and Links

const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(200))
  .force("charge", d3.forceManyBody().strength(-500))
  .force("center", d3.forceCenter(width / 2, height / 2));

const link = svg.append("g")
  .selectAll("line")
  .data(links)
  .enter().append("line")
  .attr("class", "link")
  .attr("stroke-width", d => d.thickness);

const node = svg.append("g")
  .selectAll("g")
  .data(nodes)
  .enter().append("g");

node.append("circle")
  .attr("r", 40)
  .attr("fill", d => `url(#${d.id}-img)`);

// Adjust text to support multiline via tspan
node.each(function(d) {
  const nodeD3 = d3.select(this);
  const lines = d.label.split('\n');
  const text = nodeD3.append("text")
                     .attr("dy", "-1em") // Adjust vertical spacing
                     .attr("text-anchor", "middle")
                     .style("font-size", "15px");

  lines.forEach((line, i) => {
    text.append("tspan")
        .attr("x", 0) // Center align text
        .attr("dy", `${i > 0 ? 1.2 : 0}em`) // Add space between lines, except before the first
        .text(line);
  });
});

node.append("pattern")
  .attr("id", d => `${d.id}-img`)
  .attr("patternUnits", "userSpaceOnUse")
  .attr("width", 80)
  .attr("height", 80)
  .append("image")
  .attr("xlink:href", d => d.background)
  .attr("width", 80)
  .attr("height", 80);

simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);

  node
    .attr("transform", d => `translate(${d.x},${d.y})`);
});