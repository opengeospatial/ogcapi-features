# ArcGIS Runtime APIs

This page shows an example how to connect with the ArcGIS Runtime APIs to an API that implements OGC API - Features - Part 1: Core.

## Links

- Supported APIs (https://developers.arcgis.com/documentation/mapping-apis-and-location-services/apis-and-sdks/#native-apis)
- OGCFeatureCollectionTable ([.NET](https://developers.arcgis.com/net/wpf/api-reference/html/T_Esri_ArcGISRuntime_Data_OgcFeatureCollectionTable.htm), [Android](https://developers.arcgis.com/android/api-reference/reference/com/esri/arcgisruntime/data/OgcFeatureCollectionTable.html), [iOS](https://developers.arcgis.com/ios/api-reference/interface_a_g_s_o_g_c_feature_collection_table.html), [JAVA](https://developers.arcgis.com/java/api-reference/reference/com/esri/arcgisruntime/data/OgcFeatureCollectionTable.html), [Qt](https://developers.arcgis.com/qt/qml/api-reference/qml-esri-arcgisruntime-ogcfeaturecollectiontable.html))
- Licensing and Attribution Requirements (https://developers.arcgis.com/documentation/mapping-apis-and-location-services/licensing/attribution/)


## Software version

This example uses ArcGIS Runtime 100.10 (Check out the OGC API - Features enhancements in the [Release Notes](https://developers.arcgis.com/net/reference/release-notes/#ogc-api---features)) 

## Required and supported Conformance classes

The API must at least support the [Core](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core) and [GeoJSON](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson) conformance classes.

The CRS conformance class from Part 2 (Coordinate Reference Systems by Reference) is supported, as well as, querying with cql-text and cql-json from part 3 (Filtering and the Common Query Language (CQL)).

## Description

OGC API Features is represented in the ArcGIS Runtime APIs as an OGCFeatureCollectionTable. One can create a FeatureLayer from an OGCFeatureCollectionTable and add it to the map as  shown in Sample 1. The OgcFeatureService class can be used to browse the existing collections in a service, and explore  metadata using OgcFeatureServiceInfo,  FeatureCollectionInfos, and FeatureCollectionInfo.  FeatureCollectionInfo can be used to create an OGCFeatureCollectionTable as shown in Sample 2.

.NET WPF will be used in the samples, but please note that the capabilities and class hierarchy/methods of the APIs are the same across the language/OS options offered by ArcGIS Runtime. 

### Sample 1: Use OGCFeatureCollectionTable to load, render, and query a specific collection 

<details>
  <summary>C# Code</summary>

```C#
using System;
using System.Diagnostics;
using System.Windows;
using Esri.ArcGISRuntime.Data;
using Esri.ArcGISRuntime.Geometry;
using Esri.ArcGISRuntime.Mapping;
using Esri.ArcGISRuntime.Symbology;
using Color = System.Drawing.Color;

namespace DisplayOAFeatCollection
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        // Hold a reference to the OGC feature collection table.
        private OgcFeatureCollectionTable _featureTable;

        // Constants for the service URL and collection id.
        private const string ServiceUrl = "https://demo.ldproxy.net/daraa";
        // Note that the service defines the collection id which can be accessed via OgcFeatureCollectionInfo.CollectionId. 
        private const string CollectionId = "TransportationGroundCrv";

        public MainWindow()
        {
            InitializeComponent();
            Initialize();
        }

        private async void Initialize()
        {
            // Create the map with topographic basemap.
            MyMapView.Map = new Map(Basemap.CreateTopographic());

            try
            {
                // Create the feature table from URI and collection id.
                _featureTable = new OgcFeatureCollectionTable(new Uri(ServiceUrl), CollectionId);

                // Set the feature request mode to manual - only manual is supported at v100.10.
                // In this mode, you must manually populate the table - panning and zooming won't request features automatically.
                _featureTable.FeatureRequestMode = FeatureRequestMode.ManualCache;

                // Load the table.
                await _featureTable.LoadAsync();

                // Create a feature layer to visualize the OAFeat features.
                FeatureLayer ogcFeatureLayer = new FeatureLayer(_featureTable);

                // Apply a renderer.
                ogcFeatureLayer.Renderer = new SimpleRenderer(new SimpleLineSymbol(SimpleLineSymbolStyle.Solid, Color.Blue, 3));

                // Add the layer to the map.
                MyMapView.Map.OperationalLayers.Add(ogcFeatureLayer);

                // Use the navigation completed event to populate the table with the features needed for the current extent.
                MyMapView.NavigationCompleted += MapView_NavigationCompleted;

                // Zoom to a small area within the dataset by default.
                Envelope datasetExtent = _featureTable.Extent;
                if (datasetExtent != null && !datasetExtent.IsEmpty)
                {
                    await MyMapView.SetViewpointGeometryAsync(new Envelope(datasetExtent.GetCenter(), datasetExtent.Width / 3, datasetExtent.Height / 3));
                }
            }
            catch (Exception e)
            {
                MessageBox.Show(e.ToString(), "Couldn't load sample.");
                Debug.WriteLine(e);
            }
        }

        private async void MapView_NavigationCompleted(object sender, EventArgs e)
        {
            // Show the loading bar.
            LoadingProgressbar.Visibility = Visibility.Visible;

            // Get the current extent.
            Envelope currentExtent = MyMapView.VisibleArea.Extent;

            // Create a query based on the current visible extent.
            QueryParameters visibleExtentQuery = new QueryParameters();
            visibleExtentQuery.Geometry = currentExtent;
            visibleExtentQuery.SpatialRelationship = SpatialRelationship.Intersects;
            // Set a limit of 5000 on the number of returned features per request,
            // because the default on some services could be as low as 10.
            visibleExtentQuery.MaxFeatures = 5000;

            try
            {
                // Populate the table with the query, leaving existing table entries intact.
                // Setting outFields to null requests all fields.
                await _featureTable.PopulateFromServiceAsync(visibleExtentQuery, false, null);
            }
            catch (Exception exception)
            {
                MessageBox.Show(exception.ToString(), "Couldn't populate table.");
                Debug.WriteLine(exception);
            }
            finally
            {
                // Hide the loading bar.
                LoadingProgressbar.Visibility = Visibility.Collapsed;
            }
        }
    }
}
```
</details>

<details>
  <summary>XAML Code</summary>

```XML
<Window x:Class="DisplayOAFeatCollection.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:esri="http://schemas.esri.com/arcgis/runtime/2013"
        xmlns:local="clr-namespace:DisplayOAFeatCollection"
        mc:Ignorable="d"
        Title="MainWindow" Height="450" Width="800">
    <Grid>
        <esri:MapView x:Name="MyMapView"/>
            <StackPanel>
                <TextBlock Text="Pan and zoom to see features."
                           TextAlignment="Center"
                           FontWeight="SemiBold" />
                <ProgressBar x:Name="LoadingProgressbar"
                             IsIndeterminate="True"
                             Visibility="Collapsed"
                             IsEnabled="True" />
            </StackPanel>
    </Grid>
</Window>
```
</details>

<details>
  <summary>Screenshot - pan and zoom to add more features from "TransportationGroundCrv"</summary>

  ![PanZoomToSeeFeatures](https://user-images.githubusercontent.com/3813516/112913433-6ea5c900-90ae-11eb-8f03-32535527a7ed.png)

</details>

### Sample 2: Browsing Collections using OGCFeatureService

<details>
  <summary>C# Code</summary>

```C#
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Windows;
using Esri.ArcGISRuntime.Data;
using Esri.ArcGISRuntime.Geometry;
using Esri.ArcGISRuntime.Mapping;
using Esri.ArcGISRuntime.Ogc;
using Esri.ArcGISRuntime.Symbology;
using Color = System.Drawing.Color;

namespace BrowseOAFeatServices
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        // Landing URL of the OAFeat service.
        private const string ServiceUrl = "https://demo.ldproxy.net/daraa";

        public MainWindow()
        {
            InitializeComponent();
            Initialize();
        }

        private void Initialize()
        {
            // Init the UI.
            ServiceTextBox.Text = ServiceUrl;
            // Create the map with topographic basemap.
            MyMapView.Map = new Map(Basemap.CreateTopographic());
            LoadService();
        }

        private async void LoadService()
        {
            try
            {
                LoadingProgressBar.Visibility = Visibility.Visible;
                LoadLayersButton.IsEnabled = false;
                LoadServiceButton.IsEnabled = false;

                // Create the OGC API - Features service using the landing URL.
                OgcFeatureService service = new OgcFeatureService(new Uri(ServiceTextBox.Text));

                // Load the OAFeat service.
                await service.LoadAsync();

                // Get the service metadata.
                OgcFeatureServiceInfo serviceInfo = service.ServiceInfo;

                // Get a list of available collections.
                IEnumerable<OgcFeatureCollectionInfo> layerListReversed = serviceInfo.FeatureCollectionInfos;

                // Show the layers in the UI.
                OgcFeatureCollectionList.ItemsSource = layerListReversed;
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex);
                MessageBox.Show(ex.Message, "Error loading service");
            }
            finally
            {
                // Update the UI.
                LoadingProgressBar.Visibility = Visibility.Collapsed;
                LoadLayersButton.IsEnabled = true;
                LoadServiceButton.IsEnabled = true;
            }
        }

        private async void LoadLayers_Clicked(object sender, RoutedEventArgs e)
        {
            // Skip if nothing selected.
            if (OgcFeatureCollectionList.SelectedItems.Count < 1)
            {
                return;
            }

            // Show the progress bar.
            LoadingProgressBar.Visibility = Visibility.Visible;

            // Clear the existing layers.
            MyMapView.Map.OperationalLayers.Clear();

            try
            {
                // Get the selected collection.
                OgcFeatureCollectionInfo selectedCollectionInfo = (OgcFeatureCollectionInfo)OgcFeatureCollectionList.SelectedItems[0];

                // Create the OGC feature collection table.
                OgcFeatureCollectionTable table = new OgcFeatureCollectionTable(selectedCollectionInfo);

                // Set the feature request mode to manual - only manual is supported at v100.10.
                // In this mode, you must manually populate the table - panning and zooming won't request features automatically.
                table.FeatureRequestMode = FeatureRequestMode.ManualCache;

                // Populate the OGC feature collection table.
                QueryParameters queryParamaters = new QueryParameters();
                queryParamaters.MaxFeatures = 1000;
                await table.PopulateFromServiceAsync(queryParamaters, false, null);

                // Create a feature layer from the OGC feature collection table.
                FeatureLayer ogcFeatureLayer = new FeatureLayer(table);

                // Choose a renderer for the layer based on the table.
                ogcFeatureLayer.Renderer = GetRendererForTable(table) ?? ogcFeatureLayer.Renderer;

                // Add the layer to the map.
                MyMapView.Map.OperationalLayers.Add(ogcFeatureLayer);

                // Zoom to the extent of the selected collection.
                Envelope collectionExtent = selectedCollectionInfo.Extent;
                if (collectionExtent != null && !collectionExtent.IsEmpty)
                {
                   await MyMapView.SetViewpointGeometryAsync(collectionExtent, 100);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex);
                MessageBox.Show(ex.Message, "Error loading service");
            }
            finally
            {
                // Hide the progress bar.
                LoadingProgressBar.Visibility = Visibility.Collapsed;
            }
        }

        private Renderer GetRendererForTable(FeatureTable table)
        {
            switch (table.GeometryType)
            {
                case GeometryType.Point:
                case GeometryType.Multipoint:
                    return new SimpleRenderer(new SimpleMarkerSymbol(SimpleMarkerSymbolStyle.Circle, Color.Blue, 5));

                case GeometryType.Polygon:
                case GeometryType.Envelope:
                    return new SimpleRenderer(new SimpleFillSymbol(SimpleFillSymbolStyle.Solid, Color.Blue, null));

                case GeometryType.Polyline:
                    return new SimpleRenderer(new SimpleLineSymbol(SimpleLineSymbolStyle.Solid, Color.Blue, 1));
            }

            return null;
        }

        private void LoadServiceButton_Click(object sender, RoutedEventArgs e)
        {
            LoadService();
        }
    }
}
```
</details>

<details>
  <summary>XAML Code</summary>

```XML
<Window x:Class="BrowseOAFeatServices.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:esri="http://schemas.esri.com/arcgis/runtime/2013"
        xmlns:local="clr-namespace:BrowseOAFeatServices"
        mc:Ignorable="d"
        Title="MainWindow" Height="450" Width="800">
    <Grid>        
           <Grid>
                <Grid.RowDefinitions>
                    <RowDefinition Height="Auto" />
                    <RowDefinition Height="Auto" />
                    <RowDefinition Height="Auto" />
                    <RowDefinition Height="*" />
                    <RowDefinition Height="Auto" />
                    <RowDefinition Height="Auto" />
                </Grid.RowDefinitions>
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="Auto" />
                    <ColumnDefinition Width="80*" />
                    <ColumnDefinition Width="20*" />
                </Grid.ColumnDefinitions>
            <esri:MapView x:Name="MyMapView" Margin="5" Grid.Row="2" Grid.Column="1" Grid.RowSpan="4" Grid.ColumnSpan="2"/>
               <TextBlock
                    Grid.ColumnSpan="3"
                    Margin="5"
                    FontWeight="Bold"
                    Foreground="Black"
                    Text="Load the service, then select an OGC feature collection to display."
                    TextAlignment="Center" />
                <TextBox
                    x:Name="ServiceTextBox"
                    Grid.Row="1"
                    Grid.ColumnSpan="2"
                    Margin="5" />
                <Button
                    x:Name="LoadServiceButton"
                    Grid.Row="1"
                    Grid.Column="2"
                    Margin="0,5,5,5"
                    Padding="5,0,5,0"
                    Click="LoadServiceButton_Click"
                    Content="Load service" />
                <ProgressBar                    
                    x:Name="LoadingProgressBar"
                    Grid.Row="2"
                    Grid.Column ="1"
                    Grid.ColumnSpan="2"
                    Height="10"
                    Margin="5,0,5,5"
                    IsEnabled="True"
                    IsIndeterminate="True"
                    Visibility="Visible" />
                <ListView
                    MaxWidth="350"
                    Margin="5,5,0,0"
                    x:Name="OgcFeatureCollectionList"
                    Grid.Row="2"
                    Grid.RowSpan="2"
                    Grid.ColumnSpan="1"
                    SelectionMode="Single">
                    <ListView.ItemTemplate>
                        <DataTemplate>
                            <Label Content="{Binding Title}" />
                        </DataTemplate>
                    </ListView.ItemTemplate>
                </ListView>
                <Button
                    x:Name="LoadLayersButton"
                    Grid.Row="5"
                    Click="LoadLayers_Clicked"                    
                    Margin="5,5,0,5"
                    Content="Load selected layer" />
            </Grid>
    </Grid>
</Window>
```
</details>

<details>
  <summary>Screenshot - load and browse "https://demo.ldproxy.net/daraa", select and add "Agriculture (Surfaces)"</summary>

  ![BrowseSelectAddCollection](https://user-images.githubusercontent.com/3813516/112913532-ab71c000-90ae-11eb-9857-c102b0388d50.png)

</details> 
