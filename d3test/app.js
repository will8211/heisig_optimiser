// Updated app.js

// Set canvas dimensions
const canvasWidth = 1200;
const canvasHeight = 800;

// Sample data structure
const data = {
  number: "44",
  character: "占",
  keyword: "tell fortunes",
  level: "Medium",
  id: "G",
  requirements: [
    {
      number: "43",
      character: "卜",
      keyword: "divination",
      level: null,
      id: "E",
      requirements: [
        {
          number: null,
          character: "丨",
          keyword: "walking stick",
          level: null,
          id: "C",
          requirements: [
            {
              number: "1",
              character: "一",
              keyword: "one",
              level: "Elementary",
              id: "B",
              requirements: [],
            },
          ],
        },
        {
          number: null,
          character: "丶",
          keyword: "a drop of",
          level: null,
          id: "D",
          requirements: [],
        },
      ],
    },
    {
      number: "11",
      character: "口",
      keyword: "mouth",
      level: "Elementary",
      id: "F",
      requirements: [],
    },
  ],
};

// Select the body element and append an SVG container
const mainSvg = d3
  .select("body")
  .append("svg")
  .attr("width", canvasWidth)
  .attr("height", canvasHeight);

// Function to recursively extract nodes and links
function extractNodesAndLinks(data, nodes = [], links = [], parentId = null) {
  if (!nodes.some((node) => node.id === data.id)) {
    nodes.push({
      id: data.id,
      label: `${data.character}\n${data.keyword} (${data.number})`,
      img: data.level ? `./assets/${data.level}.png` : undefined,
    });
  }

  if (parentId) {
    links.push({
      source: parentId,
      target: data.id,
      width: 2,
    });
  }

  data.requirements.forEach((req) => {
    extractNodesAndLinks(req, nodes, links, data.id);
  });
}

let graphNodes = [];
let graphLinks = [];
extractNodesAndLinks(data, graphNodes, graphLinks);

// Initialize force simulation
const forceSimulation = d3
  .forceSimulation(graphNodes)
  .force(
    "link",
    d3
      .forceLink(graphLinks)
      .id((d) => d.id)
      .distance(200)
  )
  .force("charge", d3.forceManyBody().strength(-500))
  .force("center", d3.forceCenter(canvasWidth / 2, canvasHeight / 2));

// Create edges for links
const edge = mainSvg
  .append("g")
  .attr("class", "links") // Container for all links, for better organization
  .selectAll(".link") // Use the .link class here
  .data(graphLinks)
  .enter()
  .append("line")
  .attr("class", "link") // Apply the .link class
  .attr("stroke-width", (d) => d.width);

// Create vertex groups
const vertex = mainSvg
  .append("g")
  .selectAll("g")
  .data(graphNodes)
  .enter()
  .append("g");

// Append circles for each vertex
vertex
  .append("circle")
  .attr("r", 40)
  .attr("fill", (d) => `url(#pattern-${d.id})`);

// Handle multiline text for each vertex
vertex.each(function (d) {
  const currentVertex = d3.select(this);
  const labelLines = d.label.split("\n");
  const labelText = currentVertex
    .append("text")
    .attr("dy", "-1em")
    .attr("text-anchor", "middle")
    .style("font-size", "15px");

  labelLines.forEach((line, index) => {
    labelText
      .append("tspan")
      .attr("x", 0)
      .attr("dy", `${index > 0 ? 1.2 : 0}em`)
      .text(line);
  });
});

// Append patterns for images
vertex
  .append("pattern")
  .attr("id", (d) => `pattern-${d.id}`)
  .attr("patternUnits", "userSpaceOnUse")
  .attr("width", 80)
  .attr("height", 80)
  .append("image")
  .attr("xlink:href", (d) => d.img)
  .attr("width", 80)
  .attr("height", 80)
  .on("error", function () {
    d3.select(this).attr("href", "./assets/default.png");
  }); // Fallback image on error

// Update positions on simulation tick
forceSimulation.on("tick", () => {
  edge
    .attr("x1", (d) => d.source.x)
    .attr("y1", (d) => d.source.y)
    .attr("x2", (d) => d.target.x)
    .attr("y2", (d) => d.target.y);

  vertex.attr("transform", (d) => `translate(${d.x},${d.y})`);
});
